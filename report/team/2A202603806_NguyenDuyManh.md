# Báo cáo cá nhân — Nguyễn Duy Mạnh

## 1. Thông tin thành viên

- Họ tên: Nguyễn Duy Mạnh
- MSSV: 2A202603806
- Email: prezzgts@gmail.com

## 2. Phần việc phụ trách

- **CP2, bản v2:** làm rõ mô tả tool, cách chọn tool, điền tham số và hỏi xác nhận trước khi gửi.
- **Small Local Model Challenge:** chạy hai model local, phân tích lỗi, thử v4/v5 và kiểm tra lại v5 trên cloud.
- **Eval nhóm:** xây dựng 10 case (5 single turn, 5 multi turn), chạy đánh giá và cập nhật B3, B7 cùng version log.

## 3. Đóng góp và kết quả

**Tool declaration v2:** Tôi làm rõ khi dùng/không dùng từng tool, như timeline cho tài khoản cụ thể, social_search cho chủ đề, lookup để tìm web và fetch để đọc URL. Tôi bổ sung quy ước tham số và yêu cầu hỏi lại khi thiếu thông tin hoặc chưa xác nhận gửi. V2 đạt **18/20 case (90%)**, so với baseline 70%; routing 95%, argument 90%, multiturn 100%. Hai case còn fail là R03 (từ khóa chưa đúng) và R10 (đoán tài khoản thay vì hỏi lại). Prompt hash giữa các run cũng khác, nên chưa thể nói toàn bộ mức tăng là nhờ sửa tools.

**Model local:** Tôi chạy Qwen 7B và 3B, sau đó thử hai bản prompt riêng để giữ bản cloud v3.

| Lượt chạy | Case accuracy | Kết quả chính |
|---|---:|---|
| Qwen 7B baseline | 85% | Tốt hơn 3B khi dùng cùng prompt/tools |
| Qwen 3B baseline | 60% | Còn nhầm tool, thiếu tham số và bỏ qua clarify |
| v4 local, Qwen 3B | 25% | Thêm hướng dẫn bắt buộc clarify chưa hiệu quả |
| v5 local, Qwen 3B | 70% | Rút prompt từ 739 xuống 322 từ; sửa được R06 và M02 |
| v5 trên cloud | 95% | Giữ điểm bằng v3 cloud trong lần chạy này |

V5 cải thiện tham số và giữ ngữ cảnh, nhưng routing của 3B vẫn 70%. Ở R12, model gọi send với confirmed=false; tool chặn và yêu cầu xác nhận. Vì vậy, điểm tăng chưa đủ để dùng model nhỏ tự xử lý việc gửi nội dung. Baseline local khác hash với v3 cloud nên so sánh hai bên vẫn có giới hạn.

**Eval nhóm:** Tôi xây dựng 10 case kiểm tra chọn tool, thiếu URL, xác nhận gửi và sửa yêu cầu qua nhiều lượt. Có ba case cho tool mới source_credibility và text_stats. Run cloud đạt **10/10 case pass**, không lỗi provider. Tuy nhiên, G05 vẫn viết code ngoài phạm vi dù không gọi tool; G06 và G10 gặp lỗi API X 403. Điểm 100% chỉ phản ánh những điều bộ chấm đang kiểm tra.

## 4. Bằng chứng và công cụ hỗ trợ

- Commit v2: `c0b355ff4f59db25333005a04760e2e40bbf924a` — chuẩn hóa description trong tools.yaml.
- [Tool declarations](../../starter_v0/artifacts/tools.yaml), [version log](../../starter_v0/artifacts/version_log.csv) và [run v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T184219913110.json).
- [Prompt local v4](../../starter_v0/artifacts/system_prompt_local_v4.md), [prompt local v5](../../starter_v0/artifacts/system_prompt_local_v5.md); các run và bảng so sánh nằm ở [B7 báo cáo nhóm](group_report.md#b7-small-local-model-challenge-bonus).
- [10 eval case nhóm](../../starter_v0/data/eval_group.json), [run group v3](../../starter_v0/runs/v3_B_group_openrouter_20261110T234627302520.json) và [B3 báo cáo nhóm](group_report.md#b3-team-eval-cases).
- Dùng **ChatGPT** hỗ trợ soạn/rà soát prompt, case và báo cáo; dùng **Ollama, OpenRouter** để chạy model. Kết quả được đối chiếu với summary, actual_tool_calls, actual_text và tool_results trong JSON; kiểm tra hash để biết các lượt có dùng cùng artifact không.
- Lần rà soát sau merge đã ghi nhận contract test **65 passed**. Đây là kết quả của bản sau merge, không phải test lịch sử lúc chạy v2. Lần cập nhật báo cáo này không chạy lại test hoặc eval.

## 5. Tự đánh giá

Tôi học được rằng mô tả tool cần nói rõ khi nào dùng và cách điền tham số. Thêm hướng dẫn dài chưa chắc giúp model nhỏ; cần đặt giả thuyết rồi đo lại. Khi đọc kết quả, phải xem cả nội dung phản hồi và lỗi tool vì điểm pass có thể bỏ sót hành vi ngoài phạm vi. Hướng tiếp theo là tập trung vào clarify và xác nhận gửi, giữ cố định các phần khác để so sánh rõ hơn. Tôi không phụ trách viết hai tool mới của nhóm.
