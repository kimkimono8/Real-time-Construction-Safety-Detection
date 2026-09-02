201~200~# 🦺 Real-Time Construction Safety & PPE Violation Detection (MLOps)

[![CI Pipeline](https://github.com/kimkimono8/Real-time-Construction-Safety-Detection/actions/workflows/ci.yml/badge.svg)](https://github.com/kimkimono8/Real-time-Construction-Safety-Detection/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8s-Ultralytics-00FFFF?logo=yolo&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive_UI-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)

ระบบคอมพิวเตอร์วิทัศน์ตรวจจับการสวมใส่อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคล (PPE) และแจ้งเตือนการละเมิดกฎความปลอดภัย (Violation Detection) ในไซต์งานก่อสร้างแบบ Real-Time พร้อมสถาปัตยกรรม MLOps ครบวงจรตั้งแต่ Data Pipeline, Model Training, REST API Microservice, Web UI, Containerization และ CI Pipeline

---

## 📸 Demo & Visualization

![PPE Detection Demo](docs/assets/demo.png)

ระบบมีตรรกะประเมินความปลอดภัย (Compliance Engine) แยกตามอุปกรณ์และการละเมิด:
* 🟢 **COMPLIANT:** สวมใส่อุปกรณ์ครบถ้วน (`helmet`, `vest`, `glove`, `goggles`)
* 🔴 **NON-COMPLIANT:** ตรวจพบการละเมิดความปลอดภัย (`no_helmet`, `no_vest`, `no_glove`, `no_goggles`)

---

## 📊 Model Evaluation & Benchmarks

โมเดลได้รับการ Fine-tune บนสถาปัตยกรรม **YOLOv8s (11.1M Parameters)** จำนวน 60 Epochs ประเมินผลบน Validation Set ขนาดใหญ่ (**953 ภาพ / 1,951 วัตถุ**):

| Class | Instances | Precision | Recall | mAP50 | mAP50-95 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **All Classes** | **1,951** | **55.5%** | **56.2%** | **55.1%** | **30.2%** |
| **Helmet** | 240 | 80.4% | 85.5% | **90.3%** | 70.2% |
| **Vest** | 150 | 56.2% | 60.0% | **60.9%** | 36.6% |
| **No Helmet (Violation)** | 263 | 60.8% | 62.4% | **58.4%** | 24.3% |
| **No Vest (Violation)** | 350 | 55.4% | 62.6% | **51.1%** | 22.0% |
| **Glove** | 460 | 55.8% | 62.0% | **61.5%** | 31.6% |

---

## 🏗️ System Architecture

```text
               ┌───────────────────────┐
                              │   Roboflow Universe   │ (Dataset Pipeline: 950+ Images)
                                             └───────────┬───────────┘
                                                                        │
                                                                                                   ▼
                                                                                                                  ┌───────────────────────┐
                                                                                                                                 │ YOLOv8s Fine-Tuning   │ (GPU Accelerated Training)
                                                                                                                                                └───────────┬───────────┘
                                                                                                                                                                           │
                                                                                                                                                                                        ┌─────────────┴─────────────┐
                                                                                                                                                                                                     ▼                           ▼
                                                                                                                                                                                                       ┌─────────────────────┐     ┌─────────────────────┐
                                                                                                                                                                                                         │  FastAPI Backend    │     │    Streamlit UI     │
                                                                                                                                                                                                           │  (REST API Service) │     │ (Interactive Demo)  │
                                                                                                                                                                                                             └──────────┬──────────┘     └─────────────────────┘
                                                                                                                                                                                                                          │
                                                                                                                                                                                                                                       ▼
                                                                                                                                                                                                                                         ┌─────────────────────┐
                                                                                                                                                                                                                                           │  Docker Container   │ (Production Packaging)
                                                                                                                                                                                                                                             └──────────┬──────────┘
                                                                                                                                                                                                                                                          │
                                                                                                                                                                                                                                                                       ▼
                                                                                                                                                                                                                                                                         ┌─────────────────────┐
                                                                                                                                                                                                                                                                           │ GitHub Actions CI   │ (Automated Pytest & Model Fallback)
                                                                                                                                                                                                                                                                             └─────────────────────┘# PPE Detection MLOps

Production-oriented computer vision system for detecting
personal protective equipment (PPE) in industrial environments.

## Project Goals

- Detect PPE compliance using computer vision
- Build reproducible ML training pipeline
- Track experiments and models
- Serve predictions through an API
- Containerize the application
- Automate CI/CD
- Deploy and monitor the system

## Tech Stack

- Python
- PyTorch
- YOLO
- FastAPI
- MLflow
- Docker
- GitHub Actions
- Kubernetes
- Prometheus
- Grafana

## Status

🚧 Project initialization
