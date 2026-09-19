# OcuRest - Intelligent 20-20-20 Rule Guardian

<p align="center">
  <img src="assets/icon.ico" width="96" height="96" alt="OcuRest Logo" />
</p>

<p align="center">
  <b>A lightweight, privacy-first Windows background utility that automates the 20-20-20 rule using Computer Vision and Head Pose Estimation.</b><br>
  <i>Ứng dụng chạy ngầm bảo vệ thị lực theo quy tắc 20-20-20 sử dụng Thị giác máy tính và Ước lượng hướng nhìn trên Windows.</i>
</p>

<p align="center">
  <a href="https://github.com/Baoaxid/OcuRest/releases/tag/v1.0.0"><img src="https://img.shields.io/github/v/release/Baoaxid/OcuRest?color=0f766e&label=Release" alt="Release Version"></a>
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Privacy-100%25%20Local-success" alt="Privacy">
</p>

---

## Language / Ngôn ngữ

- [English](#english)
- [Tiếng Việt](#tiếng-việt)

---

<a name="english"></a>

## English

### Overview

The **20-20-20 rule** is an ophthalmologist-recommended practice: every 20 minutes spent looking at a screen, glance at an object at least 20 feet (6 meters) away for 20 seconds to relieve ciliary muscle fatigue.

**OcuRest** monitors visual focus non-intrusively. Instead of a rigid countdown timer, it verifies whether you are actively looking at the screen via computer vision.

### Direct Download

Get the ready-to-run Windows standalone executable:

- **[Download OcuRest v1.0.0 (.exe)](https://github.com/Baoaxid/OcuRest/releases/download/v1.0.0/OcuRest.exe)** _(No Python installation required)_

### Key Features

- **Computer Vision Tracking:** MediaPipe Face Mesh & OpenCV `solvePnP` estimate head orientation (Pitch, Yaw) and Eye Aspect Ratio (EAR).
- **Conscious Rest Verification:** Distinguishes between looking at the screen and resting (turning away or voluntary eye closure).
- **Smart Reset Mechanism:** Taking a break or stepping away for >= 20 seconds automatically resets the 20-minute work timer back to `00:00`.
- **Hardware Fallback & Manual Toggle:** Automatically or manually falls back to keyboard and mouse idle monitoring (`GetLastInputInfo`) when a webcam is absent or covered.
- **Strict Privacy (Privacy-by-Design):** Video frames are processed in-memory and discarded immediately. No local storage, no network telemetry.
- **Customization & i18n:** Bilingual interface (English / Vietnamese) and custom notification sound support (`.mp3`, `.wav`).

### How It Works

| State                   | Camera Mode (Vision)                 | Input Mode (Fallback)                             |
| :---------------------- | :----------------------------------- | :------------------------------------------------ |
| **Active Work**         | User faces screen with eyes open     | Mouse movement or keypress detected within 5s     |
| **Pause (< 20s)**       | Looking away or blinking             | Inactive for < 20s (timer preserves progress)     |
| **Auto-Reset (>= 20s)** | Away / eyes closed >= 20s            | Hands off input >= 20s -> Timer resets to `00:00` |
| **Break Trigger**       | Modal dialogue + looping chime alert | Modal dialogue + looping chime alert              |

### Tech Stack

- **Language:** Python 3.9+ (64-bit)
- **Computer Vision:** OpenCV (`opencv-python`), Google MediaPipe Face Mesh
- **Math:** NumPy
- **Desktop UI:** Tkinter / TTK
- **Platform & Audio:** Windows Native APIs (`GetLastInputInfo`, `winmm.dll`) & `winsound`
- **Packaging:** PyInstaller

### Local Development Setup

```bash
# 1. Clone repository
git clone [https://github.com/Baoaxid/OcuRest.git](https://github.com/Baoaxid/OcuRest.git)
cd OcuRest

# 2. Setup virtual environment
python -m venv venv
source venv/Scripts/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Compile localization CSV to JSON
python scripts/compile_i18n.py

# 5. Run application
python main.py
```

### Packaging Standalone Executable

```cmd
build.bat
```

The standalone binary will be generated at `dist/OcuRest.exe`.

---

<a name="tiếng-việt"></a>

## Tiếng Việt

### Tổng quan

**Quy tắc 20-20-20** là khuyến nghị y khoa phổ biến: Cứ sau mỗi 20 phút nhìn màn hình, hãy nhìn xa 20 feet (khoảng 6 mét) trong 20 giây để cơ thể mi của mắt được thả lỏng và phục hồi.

**OcuRest** tự động hóa quy tắc này một cách thông minh. Thay vì dùng bộ đếm ngược thụ động, ứng dụng phân tích tư thế đầu và trạng thái mắt qua webcam để xác định thời gian nhìn màn hình thực tế.

### Tải về trực tiếp

Tải ngay bản chạy độc lập trên hệ điều hành Windows:

- **[Tải OcuRest v1.0.0 (.exe)](https://github.com/Baoaxid/OcuRest/releases/download/v1.0.0/OcuRest.exe)** _(Không yêu cầu cài đặt Python)_

### Tính năng nổi bật

- **Theo dõi thị giác máy tính:** Kết hợp MediaPipe Face Mesh và OpenCV `solvePnP` để xác định hướng mặt (Pitch, Yaw) và tỉ lệ mở mắt (EAR).
- **Phát hiện hành vi nghỉ tự nhiên:** Ghi nhận chính xác khi người dùng nhìn ra nơi khác hoặc chủ động nhắm mắt thư giãn.
- **Tự động làm mới chu kỳ (Smart Reset):** Nếu bạn nghỉ mắt hoặc rời bàn làm việc liên tục từ 20 giây trở lên, bộ đếm làm việc sẽ tự động đặt lại về `00:00`.
- **Dự phòng khi không có Camera:** Hỗ trợ tự động hoặc nhấp chuột chuyển đổi sang chế độ theo dõi qua thao tác Chuột & Bàn phím (`GetLastInputInfo`) khi máy không có webcam.
- **Bảo mật tuyệt đối (Privacy-by-Design):** Xử lý hình ảnh trực tiếp trên RAM và giải phóng tức thì; không ghi hình ảnh ra ổ đĩa, không truyền dữ liệu qua Internet.
- **Đa ngôn ngữ & Tùy biến âm thanh:** Chuyển đổi giao diện Tiếng Việt / Tiếng Anh linh hoạt và hỗ trợ nạp chuông báo riêng (`.mp3`, `.wav`).

### Cơ chế hoạt động

| Trạng thái                 | Chế độ Camera (Thị giác)         | Chế độ Chuột & Phím (Dự phòng)                       |
| :------------------------- | :------------------------------- | :--------------------------------------------------- |
| **Đang làm việc**          | Mặt nhìn màn hình và mắt đang mở | Có thao tác chuột hoặc bàn phím trong 5s gần nhất    |
| **Tạm dừng (< 20s)**       | Nhìn ra ngoài hoặc chớp mắt      | Không thao tác < 20s (bộ đếm giữ nguyên vị trí)      |
| **Tự động Reset (>= 20s)** | Rời bàn / nhắm mắt >= 20s        | Buông tay khỏi chuột/phím >= 20s -> Reset về `00:00` |
| **Chuông báo nghỉ**        | Hộp thoại thông báo + Chuông lặp | Hộp thoại thông báo + Chuông lặp                     |

### Cài đặt và Chạy mã nguồn

```bash
# 1. Kích hoạt môi trường ảo
source venv/Scripts/activate

# 2. Cài đặt các thư viện
pip install -r requirements.txt

# 3. Biên dịch file ngôn ngữ CSV sang JSON
python scripts/compile_i18n.py

# 4. Chạy ứng dụng
python main.py
```

### Đóng gói file chạy (.exe)

```cmd
build.bat
```

File thực thi độc lập sẽ nằm tại `dist/OcuRest.exe`.

---

## Project Structure / Cấu trúc thư mục

```text
OcuRest/
├─ assets/                 # Icons and media assets (.ico)
├─ csv/                    # Localization source files (app.csv)
├─ locales/                # Compiled i18n JSON files (en, vi)
├─ scripts/                # Helper tools (compile_i18n.py, pack_ico.py)
├─ src/                    # Application source code
│  ├─ audio/               # WinMM MCI audio controller
│  ├─ core/                # Configuration and resource resolution
│  ├─ platform/            # Native Win32 idle input listeners
│  ├─ ui/                  # Tkinter UI controllers and i18n loaders
│  └─ vision/              # MediaPipe Face Mesh, Head Pose & EAR
├─ .gitignore              # Git ignore configuration
├─ build.bat               # Automated build pipeline for Windows
├─ main.py                 # Application runtime entry point
├─ requirements.txt        # Runtime and build dependencies
└─ README.md               # Project documentation
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
