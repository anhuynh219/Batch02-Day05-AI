# Workshop — Mổ App AI Thật

**Người làm:** Đỗ Thị Huyền — 2A202600880
**App được mổ:** MoMo — Moni (Trợ thủ tài chính)
**Thời gian:** 35-45 phút
**Hình thức:** cá nhân trước, chia sẻ theo nhóm sau
**Output:** finding note + sketch `as-is / to-be`

Mục tiêu không phải chấm "UI đẹp hay xấu". Mục tiêu là dùng sản phẩm thật như một bài needfinding: tìm chỗ product gãy trong workflow thật, rồi viết finding đó thành quyết định product.

## 1. Sản phẩm đã chọn để dùng thử

| Sản phẩm        | AI feature                                                                                                    | Cách truy cập                            |
| --------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **MoMo — Moni** | Trợ thủ tài chính: tổng hợp & phân tích chi tiêu, trả lời câu hỏi về dòng tiền cá nhân bằng ngôn ngữ tự nhiên | App MoMo → tab "Moni / Quản lý chi tiêu" |

**Lý do chọn:** Moni hứa biến dữ liệu giao dịch thành insight tài chính, nên dễ kiểm tra xem AI có thật sự "hiểu" câu hỏi và trả lời đúng mức sâu user cần hay không.

## 2. Dùng thử: promise vs reality

**Product hứa gì?**

- Tổng hợp toàn bộ giao dịch và cho thấy **bức tranh chi tiêu**.
- Trả lời câu hỏi về tiền của user bằng ngôn ngữ tự nhiên ("tháng này tiêu nhiều nhất vào gì?").
- Biến dữ liệu giao dịch thành **insight** chứ không chỉ con số tổng.

**User nào được hứa sẽ được giúp?**

- Người dùng MoMo muốn hiểu **tiền đi đâu** mà không phải tự cộng/lọc giao dịch.

**Mình kỳ vọng AI làm được task nào?**

- Hiểu intent "nhiều nhất vào gì" = **xếp hạng chi tiêu theo danh mục**, không phải con số tổng.
- Khi câu hỏi mơ hồ ("tôi tiêu nhiều không?") thì **hỏi lại tiêu chí** thay vì tự quyết.
- Khi user yêu cầu chi tiết, đưa được **breakdown theo nhóm + số tiền từng nhóm**.

**Khi dùng thật, điểm gãy xuất hiện ở đâu?**

- Moni trả tốt câu hỏi tổng quan và câu hỏi **về một danh mục cụ thể**, nhưng **không tự tổng hợp/xếp hạng** chi tiêu theo nhiều danh mục khi user hỏi "nhiều nhất vào gì".
- Phát hiện then chốt: **dữ liệu có tồn tại** (Moni trả được "Du lịch = 0đ", "Di chuyển = 622.000đ") nhưng AI **không gộp lại thành insight** → đây là lỗi tổng hợp/intent, không phải thiếu dữ liệu.

## 3. Bốn paths (test thật trên Moni)

| Path               | Trạng thái      | Test đã chạy                                                                            | Kết quả quan sát                                                                                                                                                                                                                                              |
| ------------------ | --------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Happy**          | ✅ Đạt          | "Tháng vừa rồi tôi đã chi tiêu bao nhiêu?"                                              | Moni trả đúng & đủ: **Tổng chi tiêu 5.472.000đ · 16 giao dịch · TB 176.516đ/ngày**.                                                                                                                                                                           |
| **Low-confidence** | ⚠️ Chưa đạt     | "Tôi tiêu nhiều không?"                                                                 | Moni **tự quyết**: "So với tháng trước bạn tiêu nhiều hơn". Câu hỏi mơ hồ (so với tháng trước / thu nhập / ngân sách / người khác) nhưng Moni **không hỏi lại tiêu chí**.                                                                                     |
| **Failure**        | ❌ Fail rõ ràng | "Tháng 5 tôi chi tiêu nhiều nhất vào gì?" rồi "Hiển thị chi tiết từng nhóm với số tiền" | Cả 2 lượt Moni chỉ trả **tổng chi / số giao dịch / TB ngày**, không breakdown theo danh mục. Nhưng khi hỏi riêng "Nhóm du lịch hết bao nhiêu?" → Moni biết **Du lịch = 0đ**, **Di chuyển = 622.000đ**. ⇒ **Dữ liệu tồn tại, AI không tổng hợp được.**         |
| **Correction**     | 🟡 Đạt một phần | "Khoản 622.000đ này không phải của di chuyển"                                           | Moni không cãi, **show bằng chứng**: "Thanh toán vé tàu hỏa — 622.000đ" để user tự xác minh. ✅ không cãi user ✅ không hallucinate ✅ hiển thị evidence ✅ cho user xác minh. Còn thiếu: **chưa cho sửa nhãn ngay tại đó / chưa xác nhận có học lại không**. |

**Evidence pack**

| #   | Evidence                                                                                                                 | Loại bằng chứng         |
| --- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| E1  | Happy: hỏi tổng chi → trả 5.472.000đ / 16 GD / TB 176.516đ/ngày                                                          | Self-use, screenshot    |
| E2  | Low-confidence: "tôi tiêu nhiều không?" → Moni tự quyết "nhiều hơn tháng trước", không hỏi lại tiêu chí                  | Self-use, prompt đã thử |
| E3  | Failure: "nhiều nhất vào gì" + "chi tiết từng nhóm" → cả 2 lượt chỉ trả số tổng quan                                     | Self-use, prompt đã thử |
| E4  | Failure (đối chứng): hỏi riêng từng nhóm → Du lịch = 0đ, Di chuyển = 622.000đ ⇒ dữ liệu có sẵn nhưng không được tổng hợp | Hành vi quan sát        |
| E5  | Correction: báo sai nhóm → Moni show "Thanh toán vé tàu hỏa 622.000đ" để xác minh, không bịa                             | Self-use, screenshot    |

> Evidence ngoài self-use cần bổ sung: 1 quote review CH Play / App Store về "Moni trả lời chung chung / không chi tiết" để củng cố (tránh tự bịa).

## 4. Viết finding thành quyết định product

**Finding chính (ưu tiên 1 — Intent + Data-Tool: có dữ liệu nhưng không tổng hợp thành insight):**

```text
Khi user hỏi "tháng 5 tôi chi tiêu nhiều nhất vào gì?",
AI hiểu thành yêu cầu thống kê tổng quan và chỉ trả tổng chi/số giao dịch/TB ngày,
dù khi hỏi riêng từng nhóm thì Moni vẫn biết số liệu (Du lịch 0đ, Di chuyển 622.000đ),
hậu quả là user không nhận được câu trả lời cho intent thật (xếp hạng chi tiêu theo danh mục)
mặc dù dữ liệu đã tồn tại trong hệ thống.
Lỗi thuộc layer Intent + Data-Tool (orchestration), không phải thiếu dữ liệu.
Nên sửa bằng: map intent "nhiều nhất / vào gì / từng nhóm" -> gọi truy vấn group-by danh mục,
trả về top 3-5 nhóm kèm số tiền và %, rồi mới đưa số tổng quan như phần phụ.
Test case: "chi tiêu nhiều nhất vào gì" phải trả về danh sách nhóm đã sắp xếp giảm dần.
```

**Finding phụ 1 (ưu tiên 2 — Low-confidence: câu mơ hồ bị tự quyết):**

```text
Khi user hỏi "tôi tiêu nhiều không?" (mơ hồ: so với tháng trước/thu nhập/ngân sách),
AI tự chọn một mốc so sánh ("so với tháng trước bạn tiêu nhiều hơn") mà không hỏi lại,
hậu quả là kết luận có thể lệch ý user và user không biết con số dựa trên mốc nào.
Lỗi thuộc layer Intent + UX Recovery.
Nên sửa bằng low-confidence path: hỏi lại "Bạn muốn so với: (1) tháng trước (2) ngân sách (3) thu nhập?"
hoặc trả nhanh cả 2-3 mốc kèm nhãn rõ ràng để user tự đọc.
```

**Finding phụ 2 (điểm tốt cần GIỮ — Correction an toàn):**

```text
Khi user báo "khoản 622.000đ này không phải của di chuyển",
AI không cãi và không bịa, mà hiển thị bằng chứng "Thanh toán vé tàu hỏa 622.000đ" để user xác minh.
Đây là hành vi đúng của Correction path: minh bạch evidence + để human giữ quyền quyết định.
Cần GIỮ trong SPEC, và bổ sung: cho user sửa nhãn ngay tại đó + xác nhận correction được lưu/học lại.
```

## 5. Sketch as-is / to-be

```text
AS-IS (flow hiện tại)                          TO-BE (flow đề xuất)
-------------------------------------          -------------------------------------
User: "Tháng 5 tiêu nhiều nhất vào gì?"        User: "Tháng 5 tiêu nhiều nhất vào gì?"
        |                                              |
AI hiểu = thống kê tổng quan                   AI nhận intent = XẾP HẠNG THEO DANH MỤC  ◀ sửa intent
        |              ✗ điểm gãy 1                     |
Trả: tổng chi + số GD + TB/ngày                Gọi truy vấn GROUP-BY danh mục
        |                                       (dữ liệu vốn đã có sẵn)
User: "Chi tiết từng nhóm với số tiền"                 |
        |                                       Trả: TOP 3-5 nhóm + số tiền + %  ──┐
AI LẶP LẠI số tổng quan                                |                          │ tổng quan
        |              ✗ điểm gãy 2 (có data,           |                          │ làm phần phụ
        |                 không tổng hợp)        User: "tôi tiêu nhiều không?"     |
User hỏi lẻ từng nhóm mới ra số                 AI HỎI LẠI mốc so sánh  ◀ sửa low-confidence
        |              ✗ điểm gãy 3 (hỏi nhiều lượt)    (tháng trước / ngân sách / thu nhập)
        ▼                                              |
   Bỏ cuộc, mất niềm tin                        User báo sai nhóm → AI show evidence + cho SỬA NHÃN ◀ giữ + nâng correction
                                                       ▼
                                                User đạt mục tiêu chỉ trong 1 lượt
```

**Đọc nhanh sketch:**

- **User làm gì:** hỏi một câu mục tiêu rõ ("nhiều nhất vào gì").
- **AI làm gì:** nhận đúng intent → gọi group-by danh mục → trả breakdown trước, tổng quan sau.
- **Lúc AI không chắc (câu mơ hồ):** hỏi lại mốc so sánh thay vì tự quyết.
- **Lúc user sửa:** giữ hành vi show-evidence đang tốt, và cho sửa nhãn + lưu correction.

## 6. Tự kiểm trước khi nộp

- [x] Có observation cụ thể (5 evidence E1–E5 từ test thật trên Moni; kế hoạch bổ sung review ngoài).
- [x] Có đủ 4 paths với trạng thái thật: Happy ✅, Low-confidence ⚠️, Failure ❌, Correction 🟡.
- [x] Finding được viết thành product decision (1 finding chính + 2 finding phụ, theo layer + cách sửa + test case).
- [x] Sketch có as-is và to-be, đánh dấu 3 điểm gãy và path đã sửa.
- [x] Câu finding đổi gì trong SPEC: **SPEC phải có (1) intent-mapping cho câu hỏi phân tích ("nhiều nhất/vào gì/từng nhóm" → truy vấn group-by danh mục) trả về top nhóm + số tiền, (2) low-confidence path hỏi lại mốc so sánh cho câu mơ hồ, (3) giữ Correction kiểu show-evidence và bổ sung sửa nhãn + lưu correction** — đây là build slice trọng tâm cho prototype Day 06.
