# Báo cáo cá nhân — Đỗ Triệu Đức Phương (2A202603843)

## 1. Thông tin thành viên

- Họ tên: Đỗ Triệu Đức Phương
- MSSV: 2A202603843
- Email: 26ai.phuongdtd@vinuni.edu.vn

## 2. Phần việc phụ trách

Làm v3 cho Checkpoint 2 (CP2: Tối ưu hóa Artifacts và Prompt Engineering).

## 3. Đóng góp cụ thể

- Đề xuất và hiện thực phiên bản `v3` của CP2 với giả thuyết: phải chỉnh sửa đồng thời cả `system_prompt.md` và `tools.yaml` thì model mới đạt hiệu quả tối đa.
- Loại bỏ các chỉ dẫn sai lệch ban đầu, thêm quy tắc định tuyến (routing rules), cấm đoán mò tham số, bắt buộc hỏi xác nhận (yes_no) trước khi gửi Telegram, và chuẩn hóa quy ước đối số (clean keyword).
- Đưa độ chính xác của agent từ 70% (baseline v0) lên **95%** (v3).

## 4. Bằng chứng

- File/commit/PR: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv`.
- Run file: `starter_v0/runs/v3_B_base_openrouter_20261110T190653600689.json`.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Gemini 3.8 Flash High, kiểm tra thủ công, chạy `run_eval.py` (20/20 cases đo lường, 0 provider errors, accuracy 95%).

## 5. Tự đánh giá

Hoàn thành xuất sắc nhiệm vụ được phân công trong nhóm. Đã làm chủ việc tinh chỉnh kết hợp giữa `system_prompt` và `tools.yaml` để kiểm soát hành vi mô hình, khắc phục thành công các lỗi hallucination và vi phạm boundary.
