# OcuRest - Intelligent 20-20-20 Rule Guardian

<p align="center">
  <b>A lightweight, privacy-first Windows background utility that automates the 20-20-20 rule using Computer Vision and Head Pose Estimation.</b><br>
  <i>Ứng dụng chạy ngầm bảo vệ thị lực theo quy tắc 20-20-20 sử dụng Thị giác máy tính và Ước lượng hướng nhìn trên Windows.</i>
</p>

---

## Language / Ngôn ngữ

- [English](#english)
- [Tiếng Việt](#tiếng-việt)

---

## English

OcuRest is a Windows background utility designed to help users follow the 20-20-20 rule while working on a computer for long periods. It monitors head posture, eye state, and user activity to detect when a break is needed and automatically encourages healthier screen habits.

Instead of relying only on a rigid timer, OcuRest uses computer vision to check whether the user is truly looking at the screen. It can detect when the user turns away, closes their eyes, or is away from the desk, and it resets work time when a natural rest period is detected.

### Key Features

- Eye and head tracking with OpenCV and MediaPipe Face Mesh
- Detection of natural rest behavior such as looking away or closing eyes
- Automatic fallback to mouse and keyboard activity monitoring when the webcam is unavailable
- Smart reset of work time after a valid break
- Privacy-first design: all processing happens locally in memory
- Multi-language support for English and Vietnamese
- Custom alert sounds via .mp3 or .wav files

### Tech Stack

- Python 3.9+
- OpenCV
- MediaPipe
- NumPy
- Tkinter / TTK
- Windows API: winmm.dll, GetLastInputInfo
- PyInstaller

### System Requirements

- Windows 10/11
- Python 3.9+ 64-bit
- Webcam recommended for accurate eye and head tracking
- Basic desktop environment for normal operation

### Installation and Run

#### 1. Clone the project

```bash
git clone https://github.com/Baoaxid/OcuRest.git
cd OcuRest
```

#### 2. Create a virtual environment

##### Git Bash / Bash

```bash
python -m venv venv
source venv/Scripts/activate
```

##### Command Prompt / PowerShell

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Compile localization resources

```bash
python scripts/compile_i18n.py
```

#### 5. Run the app

```bash
python main.py
```

### Build Executable

For Windows, the project includes a build script:

```cmd
build.bat
```

Or run with Git Bash:

```bash
./build.bat
```

After the build succeeds, the executable will be generated here:

```text
dist\OcuRest.exe
```

### Main Project Structure

```text
OcuRest/
├─ assets/                # Icons and media assets
├─ csv/                   # CSV data for localization
├─ locales/               # English and Vietnamese language files
├─ scripts/               # Helper scripts
├─ src/                   # Main source code
│  ├─ audio/
│  ├─ core/
│  ├─ platform/
│  ├─ ui/
│  ├─ vision/
├─ build.bat              # Windows build script
├─ config.json            # Default app settings
├─ main.py                # Application entry point
├─ requirements.txt       # Dependency list
├─ README.md              # Project documentation
├─ OcuRest.spec           # PyInstaller config
└─ ...
```

---

## Tiếng Việt

OcuRest là một ứng dụng chạy ngầm trên Windows giúp người dùng tuân thủ nguyên tắc 20-20-20 khi làm việc trên máy tính trong thời gian dài. Ứng dụng theo dõi tư thế đầu, trạng thái mắt và hoạt động của người dùng để phát hiện khi cần nghỉ và nhắc nhở theo thói quen làm việc lành mạnh hơn.

Thay vì chỉ dựa vào bộ hẹn giờ cố định, OcuRest sử dụng thị giác máy tính để kiểm tra xem người dùng có thật sự đang nhìn vào màn hình hay không. Ứng dụng có thể nhận biết khi người dùng quay đầu, nhắm mắt hoặc rời khỏi bàn làm việc, đồng thời tự động reset thời gian làm việc khi phát hiện thời gian nghỉ hợp lý.

### Tính năng nổi bật

- Theo dõi mắt và đầu bằng OpenCV và MediaPipe Face Mesh
- Phát hiện hành vi nghỉ mắt tự nhiên như nhìn sang chỗ khác hoặc nhắm mắt
- Chuyển sang giám sát hoạt động chuột và bàn phím khi webcam không khả dụng
- Tự động reset thời gian làm việc sau khi nghỉ hợp lệ
- Thiết kế ưu tiên riêng tư: xử lý dữ liệu cục bộ trong RAM
- Hỗ trợ đa ngôn ngữ: tiếng Anh và tiếng Việt
- Có thể tùy chỉnh âm thanh cảnh báo bằng file .mp3 hoặc .wav

### Công nghệ sử dụng

- Python 3.9+
- OpenCV
- MediaPipe
- NumPy
- Tkinter / TTK
- Windows API: winmm.dll, GetLastInputInfo
- PyInstaller

### Yêu cầu hệ thống

- Windows 10/11
- Python 3.9+ 64-bit
- Nên có webcam để theo dõi mắt và đầu chính xác hơn
- Môi trường desktop cơ bản để ứng dụng hoạt động ổn định

### Cài đặt và chạy

#### 1. Clone dự án

```bash
git clone https://github.com/Baoaxid/OcuRest.git
cd OcuRest
```

#### 2. Tạo môi trường ảo

##### Git Bash / Bash

```bash
python -m venv venv
source venv/Scripts/activate
```

##### Command Prompt / PowerShell

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Cài đặt phụ thuộc

```bash
pip install -r requirements.txt
```

#### 4. Biên dịch tài nguyên ngôn ngữ

```bash
python scripts/compile_i18n.py
```

#### 5. Chạy ứng dụng

```bash
python main.py
```

### Đóng gói file exe

Trên Windows, dự án có sẵn script build:

```cmd
build.bat
```

Hoặc chạy bằng Git Bash:

```bash
./build.bat
```

Sau khi build thành công, file exe sẽ được tạo tại:

```text
dist\OcuRest.exe
```

### Cấu trúc thư mục chính

```text
OcuRest/
├─ assets/                # Icon và tài nguyên media
├─ csv/                   # Dữ liệu CSV cho đa ngôn ngữ
├─ locales/               # File dịch tiếng Anh và tiếng Việt
├─ scripts/               # Script hỗ trợ
├─ src/                   # Mã nguồn chính
│  ├─ audio/
│  ├─ core/
│  ├─ platform/
│  ├─ ui/
│  ├─ vision/
├─ build.bat              # Script build cho Windows
├─ config.json            # Cấu hình mặc định
├─ main.py                # Điểm khởi động ứng dụng
├─ requirements.txt       # Danh sách thư viện
├─ README.md              # Tài liệu dự án
├─ OcuRest.spec           # Cấu hình PyInstaller
└─ ...
```

### Lưu ý quan trọng

- Dự án hiện tối ưu cho hệ điều hành Windows.
- Chức năng phát hiện hướng nhìn phụ thuộc vào camera và điều kiện ánh sáng.
- Nếu webcam không hoạt động, ứng dụng sẽ chuyển sang chế độ dự phòng dựa trên hoạt động chuột và bàn phím.
- Dữ liệu nhạy cảm được xử lý cục bộ và không lưu trữ hình ảnh trên ổ đĩa.

### Giới hạn và mục tiêu

OcuRest nhằm hỗ trợ bảo vệ sức khỏe mắt khi làm việc lâu, đồng thời giữ trải nghiệm nhẹ, riêng tư và tự động hóa tốt nhất có thể.
