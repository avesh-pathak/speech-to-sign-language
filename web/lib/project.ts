export const GITHUB_URL =
  "https://github.com/avesh-pathak/speech-to-sign-language";

export const DOCS = {
  readme: `${GITHUB_URL}#readme`,
  architecture: `${GITHUB_URL}/blob/main/docs/ARCHITECTURE.md`,
  setup: `${GITHUB_URL}/blob/main/docs/SETUP.md`,
  paperNotes: `${GITHUB_URL}/blob/main/docs/PAPER_NOTES.md`,
  mapping: `${GITHUB_URL}/blob/main/data/mappings/telugu_to_isl.json`,
  tests: `${GITHUB_URL}/tree/main/tests`,
  issues: `${GITHUB_URL}/issues`,
  corpus: `${GITHUB_URL}/blob/main/data/README.md`,
  modelCode: `${GITHUB_URL}/blob/main/telugu_s2sl/model/res_bilstm_am.py`,
  paper: "https://doi.org/10.1109/ICSCSA66339.2025.11170908",
} as const;

export const project = {
  name: "VaniSign",
  tagline: "Telugu speech to Indian Sign Language",
  description:
    "A speech-to-sign translation framework that turns spoken Telugu into an ordered Indian Sign Language gloss sequence and plays the matching sign frames, with a text fallback that never drops a word.",
  github: GITHUB_URL,
  paper: {
    title:
      "Speech-to-Sign Language Translation Framework for Telugu Language using Residual Bidirectional LSTM with Attention Network",
    authors: "B. K. V. P. S. Mahalakshmi and S. Anuradha",
    venue: "ICSCSA 2025",
    doi: "10.1109/ICSCSA66339.2025.11170908",
  },
  runtime: {
    asr: "Google Speech Recognition · te-IN",
    audio: "16 kHz mono",
    dictionaryEntries: 214,
    frameFormats: ["jpg", "jpeg", "png"],
    playbackFps: 10,
    fallbackMs: 900,
    display: "400 × 400",
    interface: "Tkinter",
  },
  model: {
    input: "200 × 143",
    featureCount: 143,
    features: [
      { label: "MFCC + Δ + ΔΔ", count: 120 },
      { label: "Spectral", count: 4 },
      { label: "Spectral contrast", count: 7 },
      { label: "Chroma", count: 12 },
    ],
    attentionHeads: 4,
    bilstmUnits: "128 × 2",
    denseUnits: 256,
    dropout: 0.3,
    optimizer: "Adam 1e-3",
    loss: "Sparse categorical cross-entropy",
    split: "75 / 25",
  },
  stack: [
    {
      group: "Runtime",
      note: "No GPU",
      items: [
        { name: "Python", role: "Language runtime", version: "3.10–3.12" },
        { name: "Tkinter", role: "Desktop interface", version: "stdlib" },
        { name: "NumPy", role: "Array + feature maths", version: "1.24+" },
        { name: "Pillow", role: "Frame decoding", version: "10.0+" },
        { name: "imageio", role: "Optional GIF fallback", version: "2.31+" },
      ],
    },
    {
      group: "Speech & language",
      note: "Online path",
      items: [
        { name: "SpeechRecognition", role: "Microphone + audio input", version: "3.10+" },
        { name: "PyAudio", role: "Platform audio capture", version: "system" },
        { name: "Google ASR", role: "Telugu recognition", version: "te-IN" },
        { name: "librosa", role: "Audio decode + features", version: "0.10+" },
        { name: "SoundFile", role: "WAV I/O", version: "0.12+" },
        { name: "deep-translator", role: "Telugu → English pivot", version: "1.11+" },
      ],
    },
    {
      group: "Model & quality",
      note: "Optional",
      items: [
        { name: "TensorFlow", role: "Model + training", version: "2.13+" },
        { name: "Keras", role: "Layers + callbacks", version: "2.13+" },
        { name: "scikit-learn", role: "Split + metrics", version: "1.3+" },
        { name: "tqdm", role: "Training progress", version: "4.65+" },
        { name: "pytest", role: "Offline test suite", version: "7.4+" },
      ],
    },
  ],
  capabilities: [
    {
      name: "Runtime pipeline",
      path: "telugu_s2sl/pipeline.py",
      description:
        "One orchestration seam returns source text, token records, ISL glosses, and playback records as a single bundle. The GUI and CLI cannot drift because they call the same object.",
      tags: ["GUI", "CLI", "Tests"],
    },
    {
      name: "Curated mapping",
      path: "data/mappings/telugu_to_isl.json",
      description:
        "A hand-checked 214-entry Telugu → ISL dictionary, plus generated corpus lookups. The mapping is data, not code, so adding another sign language stays possible.",
      tags: ["214 entries", "JSON"],
    },
    {
      name: "Acoustic model",
      path: "telugu_s2sl/model/res_bilstm_am.py",
      description:
        "Dual features feed a residual BiLSTM with multi-head attention. The full training and inference path is implemented; no pretrained checkpoint is claimed.",
      tags: ["143-D", "4 heads", "TF / Keras"],
    },
    {
      name: "Frame animator",
      path: "telugu_s2sl/animation/corpus.py",
      description:
        "Indexes sign directories, sorts frames by number, caches decoded images, and returns ordered playback records. Missing directories become text cards instead of crashes.",
      tags: ["Lazy load", "Cache"],
    },
    {
      name: "Desktop app",
      path: "telugu_s2sl/gui/app.py",
      description:
        "A deliberately plain Tkinter window: record, upload, or type on the left; a 400 × 400 sign display and playback controls on the right. The animation stays the focus.",
      tags: ["Tkinter", "~10 fps"],
    },
    {
      name: "Offline test suite",
      path: "tests/",
      description:
        "Six pytest modules cover features, translation, animation, the end-to-end pipeline, the model forward pass, and Telugu text helpers. No corpus or network required.",
      tags: ["6 modules", "pytest"],
    },
  ],
} as const;

export type Project = typeof project;
