
import streamlit as st
import librosa
import numpy as np
import plotly.graph_objs as go
import schemdraw
import schemdraw.elements as elm


def draw_lowpass():
    with schemdraw.Drawing(show=False) as d:
        d += elm.SourceSin().up().label('In')
        d += elm.Resistor().right().label('R')
        d += elm.Capacitor().down().label('C')
        d += elm.Line().left()
        d += elm.Ground()
        d += elm.Line().up().at(d.elements[1].end).dot()
        d += elm.Line().right().label('Out')
        return d.get_imagedata('svg')

def draw_highpass():
    with schemdraw.Drawing(show=False) as d:
        d += elm.SourceSin().up().label('In')
        d += elm.Capacitor().right().label('C')
        d += elm.Resistor().down().label('R')
        d += elm.Ground()
        d += elm.Line().up().at(d.elements[1].end).dot()
        d += elm.Line().right().label('Out')
        return d.get_imagedata('svg')

def draw_limiter():
    with schemdraw.Drawing(show=False) as d:
        d += elm.SourceSin().up().label('In')
        d += elm.Resistor().right().label('R')
        d += elm.Diode().right().label('D1')
        d += elm.Diode().down().reverse().label('D2')
        d += elm.Line().left()
        d += elm.Ground()
        d += elm.Line().up().at(d.elements[1].end).dot()
        d += elm.Line().right().label('Out')
        return d.get_imagedata('svg')

def draw_noise_gate():
    # MVP: Simple representation (just input, block, output)
    with schemdraw.Drawing(show=False) as d:
        d += elm.SourceSin().up().label('In')
        d += elm.Opamp().right().label('Noise Gate\n(Op-Amp Comparator)')
        d += elm.Line().right().label('Out')
        return d.get_imagedata('svg')


st.set_page_config(page_title="Analog Circuit Sound Designer", page_icon="🎸", layout="wide")

st.markdown("# 🎸 Analog Circuit Sound Designer")
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if audio_file:
    y, sr = librosa.load(audio_file, sr=None)
    st.write(f"Sample Rate: `{sr} Hz` &nbsp;&nbsp; Duration: `{len(y)/sr:.2f} seconds`")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Audio Features")
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        avg_centroid = np.mean(spectral_centroids)
        st.write(f"**Spectral Centroid:** `{avg_centroid:.2f} Hz`")
        rms = librosa.feature.rms(y=y)[0]
        avg_rms = np.mean(rms)
        st.write(f"**RMS Energy:** `{avg_rms:.4f}`")
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        avg_zcr = np.mean(zcr)
        st.write(f"**Zero Crossing Rate:** `{avg_zcr:.4f}`")
        S, phase = librosa.magphase(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr)
        bass_energy = np.sum(S[freqs < 250])
        treble_energy = np.sum(S[freqs > 2500])
        ratio = bass_energy / treble_energy if treble_energy > 0 else 0
        st.write(f"**Bass/Treble Ratio:** `{ratio:.4f}`")

        # ====== SUGGESTED CIRCUIT LOGIC GOES HERE ======
        st.markdown("### 🎛️ Suggested Analog Circuit")
        suggestions = []
        if avg_centroid > 3000:
            suggestions.append("Low-Pass RC Filter (to tame brightness)")
        elif avg_centroid < 1000:
            suggestions.append("High-Pass RC Filter (to boost clarity)")
        if avg_zcr > 0.1:
            suggestions.append("Noise Gate (to reduce hiss/noise)")
        if avg_rms > 0.2:
            suggestions.append("Limiter or Soft Clipping Distortion (to control loudness)")
        if ratio > 2.0:
            suggestions.append("Bass Cut EQ (to balance spectrum)")
        elif ratio < 0.5:
            suggestions.append("Treble Cut EQ (to balance spectrum)")
        if len(suggestions) == 0:
            suggestions.append("Bypass (No processing needed—your audio is well-balanced!)")
        for s in suggestions:
            st.success(f"**{s}**")
        # =================================================

        # --- Show Live Schematic for First Detected Effect ---
        st.markdown("#### 🖼️ Schematic Diagram")

        def render_svg(svg_bytes_or_str):
            if isinstance(svg_bytes_or_str, bytes):
                svg_str = svg_bytes_or_str.decode("utf-8")
            else:
                svg_str = svg_bytes_or_str
            st.markdown(svg_str, unsafe_allow_html=True)

        if "Low-Pass RC Filter" in suggestions[0]:
            svg = draw_lowpass()
            render_svg(svg)
        elif "High-Pass RC Filter" in suggestions[0]:
            svg = draw_highpass()
            render_svg(svg)
        elif "Limiter or Soft Clipping Distortion" in suggestions[0]:
            svg = draw_limiter()
            render_svg(svg)
        elif "Noise Gate" in suggestions[0]:
            svg = draw_noise_gate()
            render_svg(svg)
        else:
            st.info("No schematic available for this effect (yet!).")

    with col2:
        # Downsample for fast plotting
        max_points = 4000
        if len(y) > max_points:
            idx = np.linspace(0, len(y) - 1, max_points).astype(int)
            y_plot = y[idx]
            times_plot = np.arange(len(y))[idx] / sr
        else:
            y_plot = y
            times_plot = np.arange(len(y)) / sr
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times_plot, y=y_plot, mode='lines', name='Waveform'))
        fig.update_layout(
            title='Waveform (zoom/pan!)',
            xaxis_title='Time (s)',
            yaxis_title='Amplitude',
            showlegend=False,
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 Upload a WAV or MP3 file to get started!")
