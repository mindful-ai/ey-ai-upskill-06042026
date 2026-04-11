# Hugging Face Transformers --- Summary Guide (Extended)

## Overview

This document provides a structured summary of Hugging Face
Transformers, including task classifications, model classes, real-world
applications, and a decision tree for model selection.

------------------------------------------------------------------------

# NLP (Text)

  ---------------------------------------------------------------------------------------------------------------
  Task             Pipeline Task Name     Model Class                          Example Models   Real-World Uses
  ---------------- ---------------------- ------------------------------------ ---------------- -----------------
  Text             text-classification    AutoModelForSequenceClassification   BERT, RoBERTa    Sentiment
  Classification                                                                                analysis, spam
                                                                                                detection

  Token            token-classification   AutoModelForTokenClassification      BERT-NER         Named Entity
  Classification                                                                                Recognition

  Question         question-answering     AutoModelForQuestionAnswering        BERT-QA          Chatbots,
  Answering                                                                                     document QA

  Text Generation  text-generation        AutoModelForCausalLM                 GPT, LLaMA       Chat systems

  Seq2Seq          text2text-generation   AutoModelForSeq2SeqLM                T5, BART         Translation,
  Generation                                                                                    summarization

  Fill Mask        fill-mask              AutoModelForMaskedLM                 BERT             Autocomplete

  Sentence         feature-extraction     AutoModel                            Sentence-BERT    Semantic search
  Similarity                                                                                    

  Summarization    summarization          AutoModelForSeq2SeqLM                BART, T5         Article
                                                                                                summarization

  Translation      translation            AutoModelForSeq2SeqLM                MarianMT         Language
                                                                                                translation
  ---------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Speech / Audio

  --------------------------------------------------------------------------------------------------------------------
  Task             Pipeline Task Name             Model Class                       Example Models   Real-World Uses
  ---------------- ------------------------------ --------------------------------- ---------------- -----------------
  Speech           automatic-speech-recognition   AutoModelForSpeechSeq2Seq / CTC   Whisper,         Transcription
  Recognition                                                                       Wav2Vec2         

  Audio            audio-classification           AutoModelForAudioClassification   AST              Sound detection
  Classification                                                                                     

  Text-to-Speech   text-to-speech                 AutoModelForTextToWaveform        Bark, VITS       Voice synthesis

  Audio-to-Audio   audio-to-audio                 Varies                            Enhancement      Noise reduction
                                                                                    models           
  --------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Vision (CV)

  -------------------------------------------------------------------------------------------------------------
  Task             Pipeline Task Name     Model Class                        Example Models   Real-World Uses
  ---------------- ---------------------- ---------------------------------- ---------------- -----------------
  Image            image-classification   AutoModelForImageClassification    ViT, ResNet      Object
  Classification                                                                              recognition

  Object Detection object-detection       AutoModelForObjectDetection        DETR, YOLO       Autonomous
                                                                                              systems

  Image            image-segmentation     AutoModelForSemanticSegmentation   SegFormer        Medical imaging
  Segmentation                                                                                

  Image Captioning image-to-text          VisionEncoderDecoder               BLIP             Accessibility
  -------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Multimodal

  --------------------------------------------------------------------------------------------------
  Task       Pipeline Task Name            Model Class            Example Models   Real-World Uses
  ---------- ----------------------------- ---------------------- ---------------- -----------------
  Visual QA  visual-question-answering     Vision+Text            BLIP, LLaVA      Image
                                                                                   understanding

  Document   document-question-answering   LayoutLM               LayoutLMv3       Invoice parsing
  QA                                                                               

  Image +    image-to-text                 VisionEncoderDecoder   Donut            OCR-free
  Text                                                                             extraction
  --------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Tabular / Other

  -------------------------------------------------------------------------------------
  Task            Pipeline Task Name   Model Class   Example Models   Real-World Uses
  --------------- -------------------- ------------- ---------------- -----------------
  Feature         feature-extraction   AutoModel     Any encoder      Embeddings
  Extraction                                                          

  Reinforcement   N/A                  Custom        Decision         Robotics
  Learning                                           Transformers     
  -------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Key Design Abstractions

  Component       Purpose
  --------------- --------------------------
  pipeline()      High-level API
  AutoModel\*     Task-specific loaders
  AutoTokenizer   Text preprocessing
  AutoProcessor   Multimodal preprocessing
  Trainer         Training loop
  Datasets        Data handling

------------------------------------------------------------------------

# How to Choose

-   Classification → AutoModelForSequenceClassification\
-   Generation → AutoModelForCausalLM\
-   Translation/Summarization → AutoModelForSeq2SeqLM\
-   Speech → AutoModelForSpeechSeq2Seq\
-   Vision → AutoModelForImageClassification

------------------------------------------------------------------------

# Decision Tree for Model Selection

    Start
     │
     ├── Is your input text?
     │     ├── Yes
     │     │     ├── Need classification? → SequenceClassification (BERT)
     │     │     ├── Need generation?
     │     │     │     ├── Open-ended → CausalLM (GPT, LLaMA)
     │     │     │     └── Structured → Seq2SeqLM (T5, BART)
     │     │     ├── Need QA? → QuestionAnswering
     │     │     └── Need embeddings? → AutoModel / Sentence-BERT
     │
     ├── Is your input audio?
     │     ├── Speech-to-text → SpeechSeq2Seq (Whisper)
     │     ├── Classification → AudioClassification
     │     └── TTS → TextToWaveform
     │
     ├── Is your input image?
     │     ├── Classification → ImageClassification
     │     ├── Detection → ObjectDetection
     │     ├── Segmentation → SemanticSegmentation
     │     └── Captioning → VisionEncoderDecoder
     │
     └── Multimodal?
           ├── Image + Text → VQA (BLIP, LLaVA)
           └── Documents → LayoutLM

------------------------------------------------------------------------

# Production Insights

-   Use pipelines for prototyping\
-   Use model classes for control\
-   Optimize with quantization, ONNX, TensorRT

------------------------------------------------------------------------

# Mental Model

    Task → Pipeline → Model Class → Pretrained Model → Deployment
