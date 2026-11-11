# Báo cáo cá nhân — Vũ Xuân Bách (2A202603803)

## 1. Thông tin thành viên

- Họ tên: Vũ Xuân Bách
- MSSV: 2A202603803
- Email: 26ai.bachvx2@vinuni.edu.vn
- Vai trò: Leader

## 2. Phần việc phụ trách

- **Leader**: Điều phối nhóm, phân chia công việc, tổng hợp thông tin.
- **CP1 & CP2 (v0, v1)**:
  - Thiết lập baseline `v0` ban đầu trên benchmark `eval_base.json`.
  - Tối ưu hóa phiên bản `v1` cho Checkpoint 2 (CP2) tập trung vào `system_prompt.md`.
- **Phát triển UI & Deployment**:
  - Xây dựng giao diện chat đa lượt trực quan với Streamlit (`starter_v0/app.py`).
  - Thiết lập public endpoint phục vụ Team Showdown qua Cloudflare Tunnel.
- **Tổng hợp Báo cáo nhóm (`group_report.md`)**:
  - Thu thập số liệu, đối chiếu bằng chứng thực tế từ run JSON, transcript và unit test để hoàn thiện toàn diện báo cáo nhóm.

## 3. Đóng góp cụ thể

- **Chạy Baseline v0**:
  - Chạy đánh giá ban đầu trên `eval_base.json` với model `nvidia/nemotron-3.5-super-vl:free` (OpenRouter), ghi nhận case accuracy cơ sở đạt 70%.
  - Phân tích các pattern lỗi chính: model đoán mò khi thiếu handle/URL (`R10`, `R11`), trích xuất câu tiếng Việt vào `query` (`R03`), vi phạm boundary tự gửi tin nhắn khi chưa xác nhận (`R12`).
- **Phát triển và đánh giá v1**:
  - Đề xuất giả thuyết: "Cho model tự tra cứu, hỏi khi thiếu thông tin cốt lõi, không bịa nguồn và yêu cầu người dùng xác nhận trước các hành động không thể hoàn tác sẽ giảm việc bịa đầu vào và giảm các lần gửi/đăng ngoài ý muốn."
  - Chỉnh sửa `system_prompt.md`, nâng case accuracy từ 70% lên 75%, loại bỏ được lỗi nhét time expression vào query của multi-turn (`M02`).
- **Xây dựng UI Streamlit (`starter_v0/app.py`)**:
  - Thiết kế giao diện hỗ trợ trò chuyện trực tiếp với Agent, hiển thị chi tiết các tool calls (tên tool, đối số, kết quả trả về) theo thời gian thực.
  - Tích hợp đúng contract với `OpenRouterProvider.complete()` và cơ chế xử lý tương tác chờ phản hồi của người dùng (`awaiting_user`) khi tool `clarify` được gọi.
  - Hỗ trợ lưu trữ lịch sử hội thoại tự động ra file transcript chuẩn.
- **Triển khai Cloudflare Tunnel**:
  - Tải và cấu hình `cloudflared` trên macOS (ARM64), mở tunnel public an toàn cho phép ban giám khảo và các team khác truy cập dùng thử UI ngay lập tức tại: `https://geography-adaptive-leaves-unfortunately.trycloudflare.com`.
- **Tổng hợp & hoàn thiện Báo cáo nhóm**:
  - Biên soạn và hoàn thiện đầy đủ cả Phần A (giới thiệu, công cụ, hướng dẫn sử dụng) và Phần B (bằng chứng thực tế B1–B7, bảng phân tích failure analysis, kết quả model local và unit tests).

## 4. Bằng chứng

- **Files / Code**:
  - Artifacts: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/version_log.csv`.
  - UI Application: `starter_v0/app.py`.
  - Report: `report/team/group_report.md`.
- **Runs / Bằng chứng thực nghiệm**:
  - `starter_v0/runs/v0_B_base_openrouter_20261110T172108091238.json` (v0 baseline: accuracy 70%, 20/20 cases đo thành công).
  - `starter_v0/runs/v1_B_base_openrouter_20261110T193325762444.json` (v1 prompt: accuracy 75%, 20/20 cases đo thành công).
- **Public URL**: `https://geography-adaptive-leaves-unfortunately.trycloudflare.com`.

## 5. Tự đánh giá

Tôi nhận thấy việc LLM chọn đúng tool và điền đúng tham số phụ thuộc nhiều vào mô tả tool: cần nêu rõ khi nào dùng, khi nào không dùng và quy ước điền tham số để model không chọn nhầm hay đoán bừa. Tôi cũng nhận thấy prompt quá dài không giúp ích mà còn làm model nhỏ bị phân tâm, trong khi bản rút gọn tập trung vào quy tắc cốt lõi cho kết quả tốt hơn rõ rệt. Cuối cùng, khi đánh giá, tôi không thể chỉ dựa vào điểm pass hay độ chính xác của benchmark tự động mà phải kiểm tra thêm nội dung model sinh ra và phản hồi lỗi từ tool, vì điểm pass có thể bỏ sót các hành vi ngoài phạm vi hoặc lỗi quyền truy cập API.

