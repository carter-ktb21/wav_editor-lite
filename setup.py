from setuptools import setup

setup(
    name="wav_editor-lite",
    version="0.1.0",
    python_requires=">=3.12",
    packages=['wav_editor-lite'],
    license='MIT',
    install_requires=[
        "pydub>=0.27.1",
        "numpy>=1.25.2",
        "imageio-ffmpeg>=0.4.10"
    ],
    description="A lightweight Python WAV editor via json data",
    url="https://github.com/carter-ktb21/wav_editor-lite.git",
)