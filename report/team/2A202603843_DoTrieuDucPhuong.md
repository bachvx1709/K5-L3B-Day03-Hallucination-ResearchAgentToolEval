# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Đỗ Triệu Đức Phương
- MSSV: 2A202603843
- Email: 26ai.phuongdtd@vinuni.edu.vn

## 2. Phần việc phụ trách

- **Checkpoint 2 (CP2) — Tối ưu hóa prompt và tool declaration (Phiên bản v3)**:
  - Phân tích sâu các lỗi thất bại (failure cases) còn tồn đọng sau các phiên bản v0, v1, v2 (đặc biệt là các lỗi `wrong_arg_value`, `wrong_boundary`, và `missing_tool_call`).
  - Xây dựng và kiểm chứng giả thuyết tối ưu hóa toàn diện: kết hợp đồng thời việc tái cấu trúc `system_prompt.md` và chuẩn hóa khai báo `tools.yaml`.
  - Loại bỏ triệt để các chỉ dẫn xấu cố ý (bad instructions) của starter code trong system prompt (chỉ dẫn xúi đoán bừa, tự ý gửi tin mà không xin phép, ép hoàn thành trong 1 bước).
  - Bổ sung hệ thống quy tắc điều hướng (Routing Rules), phân định ranh giới an toàn (Guardrails / Boundary), chuẩn hóa quy ước truyền tham số (Argument Conventions) và xử lý ngữ cảnh đa lượt (Multi-turn Context Carryover).
  - Thực hiện chạy base evaluation cho version v3, phân tích kết quả đo lường và ghi nhận bằng chứng đầy đủ vào `version_log.csv`.

## 3. Đóng góp cụ thể

1. **Phát triển giả thuyết và chiến lược tối ưu hóa toàn diện cho Version 3 (v3)**:
     - *"Tối ưu hóa đồng thời cả `artifacts/system_prompt.md` (loại bỏ toàn bộ chỉ dẫn xúi đoán mò, bổ sung routing rules, quy định ranh giới xác nhận) và `artifacts/tools.yaml` (viết lại description nêu rõ khi nào dùng / khi nào không dùng, chuẩn hóa convention cho tham số screenname không chứa `@`, query chỉ chứa từ khóa thực thể, định danh topic/timeframe/search_type, thiết lập boundary confirmed=true cho send) sẽ loại bỏ triệt để các lỗi hallucination/argument mismatch, đưa độ chính xác routing và arguments lên mức tối đa."*

2. **Tái cấu trúc và chuẩn hóa `starter_v0/artifacts/system_prompt.md`**:
   - **Xóa bỏ các chỉ dẫn xấu**: Loại bỏ hoàn toàn các prompt xúi giục đoán bừa tài khoản người nổi tiếng (như Sam Altman), đoán mò URL, tự động gửi tin không chờ xác nhận, và ép thực hiện trong 1 bước duy nhất.
   - **Xây dựng nguyên tắc cốt lõi (Core Principles & Guardrails)**:
     - *Nguyên tắc bảo vệ thông tin thiếu*: Khi thiếu thông tin thiết yếu (tên tài khoản Twitter, URL bài viết), bắt buộc phải gọi `clarify` với `response_type: "text"`, tuyệt đối không đoán mò.
     - *Nguyên tắc ranh giới an toàn (Safety Boundary)*: Đối với hành động ghi/gửi tin nhạy cảm, bắt buộc phải gọi `clarify` với `response_type: "yes_no"` để người dùng xác nhận trước; chỉ gọi `send` khi người dùng đã đồng ý (`confirmed: true`).
     - *Phân biệt yêu cầu ngoài phạm vi & meta*: Tự trả lời các câu hỏi về bản thân và từ chối các yêu cầu ngoài phạm vi nghiên cứu (giải toán tích phân, viết code đệ quy) bằng văn bản mà không gọi tool bừa bãi.
     - *Quy tắc gọi song song (Parallel Tool Calls)*: Tự động kích hoạt đồng thời nhiều tool (ví dụ: vừa tìm web vừa tìm tweet) khi người dùng yêu cầu đa nguồn trong cùng một truy vấn.
     - *Duy trì ngữ cảnh hội thoại đa lượt (Multi-turn Context)*: Kế thừa chính xác các tham số từ các lượt trước (timeframe, topic, limit) trừ khi người dùng yêu cầu thay đổi.
   - **Chi tiết hóa quy tắc điều hướng (Routing Rules)** cho từng công cụ: `clarify`, `timeline`, `social_search`, `lookup`, `fetch`, `send`, `format`, `policy`, `papers`, `paper_text`. Đặc biệt lưu ý trích xuất `query` sạch (loại bỏ các từ chỉ thời gian như 'hôm nay', 'tuần này' hay từ loại tin như 'tin tức', 'nổi bật').

3. **Viết lại toàn bộ khai báo schema trong `starter_v0/artifacts/tools.yaml`**:
   - Viết lại phần `description` của tất cả các công cụ theo cấu trúc: **Làm gì, DÙNG KHI NÀO và KHÔNG DÙNG KHI NÀO**.
   - Chuẩn hóa các quy ước tham số (Argument Conventions) trong phần mô tả của từng thuộc tính:
     - `timeline`: Quy định rõ `screenname` là handle không chứa tiền tố `@` (ví dụ: `sama`, `elonmusk`, `karpathy`); ánh xạ đúng tên người sang handle.
     - `lookup`: Quy định nghiêm ngặt tham số `query` chỉ chứa từ khóa hoặc thực thể cốt lõi; phân loại rõ `topic` (`news` cho tin thời sự/công nghệ, `general` cho kiến thức chung); chuẩn hóa `timeframe` (`day` cho hôm nay, `week` cho tuần này).
     - `social_search`: Hướng dẫn sử dụng `search_type: "Top"` cho bài đăng nổi bật/phổ biến và `Latest` cho bài đăng mới nhất.
     - `send`: Mô tả chặt chẽ boundary xác nhận; tham số `confirmed` bắt buộc phải là `true` mới được thực thi, nếu chưa xác nhận phải thông qua `clarify`.
   - Bảo đảm tương thích 100% với chữ ký hàm trong mã nguồn Python, vượt qua toàn bộ 55/55 test hợp đồng (`test_tool_contract.py`).

4. **Đo lường, kiểm thử và ghi nhận kết quả thực nghiệm**:
   - Chạy kiểm thử tự động với OpenRouter (`nvidia/nemotron-3.5-super-vl:free`) trên bộ 20 case tiêu chuẩn `data/eval_base.json`.
   - Kết quả đo lường thực tế của version v3:
     - **Case Accuracy**: Tăng vọt từ **0.70 (v0) lên 0.95 (19/20 cases passed)**.
     - **Tool Routing Accuracy**: Đạt mức hoàn hảo **1.0 (100%)**.
     - **Argument Accuracy**: Đạt **0.95 (95%)**.
     - **Multiturn Accuracy**: Đạt mức hoàn hảo **1.0 (100%)**.
     - **Provider Error Cases**: **0**.
   - Cập nhật nhật ký phát triển vào `starter_v0/artifacts/version_log.csv` với đầy đủ artifact version, mã băm sha256 (`prompt_hash`, `tools_hash`), giả thuyết, lý do thay đổi và đường dẫn run file chứng cứ.

## 4. Bằng chứng

- **Mã nguồn và artifacts đã thực hiện**:
  - `starter_v0/artifacts/system_prompt.md`: Bản prompt tối ưu hóa cho v3.
  - `starter_v0/artifacts/tools.yaml`: Bản schema chuẩn hóa đầy đủ description, convention args và boundary.
  - `starter_v0/artifacts/version_log.csv`: Ghi nhận nhật ký thực nghiệm v3 (`v3+pdd22a4e2a8aa+t141d5f5ff0e9`).
  - `starter_v0/runs/v3_B_base_openrouter_20261110T190653600689.json`: File kết quả chạy eval thực tế của v3 chứng minh độ chính xác 95%.
- **Dữ liệu thực nghiệm cụ thể (trích từ `version_log.csv`)**:
  - `Version`: v3
  - `Author`: Phương
  - `Changed Artifact`: `system_prompt.md, tools.yaml`
  - `Prompt Hash`: `dd22a4e2a8aacbf393abf9b68b4c4be918f1c7beec7dc047cad01fed8c65c91b`
  - `Tools Hash`: `141d5f5ff0e9f3b001c9d46c1a77c5a0b6b2282d903c4832d4a33ec2457637ee`
  - `Metric Before -> After`: `0.70 -> 0.95`
- **Công cụ và AI đã sử dụng**:
  - Sử dụng trợ lý AI (Gemini 3.8 Flash High) để hỗ trợ rà soát logic routing, phát hiện mâu thuẫn giữa mô tả prompt và schema YAML, và xây dựng các mệnh đề ràng buộc chặt chẽ.
  - Tự kiểm tra: Chạy lệnh `pytest tests/test_tool_contract.py` kiểm tra schema hợp đồng, chạy lệnh `python run_eval.py --provider openrouter --version v3 --suite base` kiểm tra độ chính xác thực tế trên 20 test cases.

## 5. Tự đánh giá

- Hoàn thành xuất sắc nhiệm vụ của Checkpoint 2 (CP2), đóng góp cốt lõi vào các tiêu chí chấm điểm chính:
  - **Tiêu chí C2 (15/15 điểm)**: Tối ưu hoàn chỉnh system prompt và tool declarations, loại bỏ chỉ dẫn xấu, có routing rules và arg conventions rõ ràng, contract test xanh 100%.
  - **Tiêu chí C3 (20/20 điểm)**: Thực hiện đúng quy trình khoa học của vòng lặp giả thuyết → sửa đổi → thực nghiệm đo lường, nâng accuracy của agent từ 70% lên 95% có file run JSON bằng chứng đầy đủ.



