# Workshop — Mổ App AI Thật

**Thời gian:** 35-45 phút  
**Hình thức:** cá nhân trước, chia sẻ theo nhóm sau  
**Output:** finding note + sketch `as-is / to-be`

Mục tiêu không phải chấm "UI đẹp hay xấu". Mục tiêu là dùng sản phẩm thật như một bài needfinding: tìm chỗ product gãy trong workflow thật, rồi viết finding đó thành quyết định product.

## 1. Chọn một sản phẩm để dùng thử

| Sản phẩm | AI feature | Cách truy cập |
|---|---|---|
| MoMo — Moni | Trợ thủ tài chính, phân tích chi tiêu, chatbot | App MoMo |
| Vietnam Airlines — NEO | Chatbot hỗ trợ vé, hành lý, khiếu nại | Website/Zalo VNA |
| V-App — V-AI | Trợ lý voice/text, gợi ý theo ngữ cảnh | App V-App |

## 2. Dùng thử: promise vs reality

Ghi nhanh:

- Product hứa gì?
- User nào được hứa sẽ được giúp?
- Bạn kỳ vọng AI làm được task nào?
- Khi dùng thật, điểm gãy xuất hiện ở đâu?

Evidence cần có:

- screenshot,
- quote từ app/web/review,
- prompt/input đã thử,
- hành vi quan sát được.

## 3. Vẽ 4 paths

| Path | Câu hỏi cần trả lời |
|---|---|
| Happy | Khi AI đúng và tự tin, user thấy gì? |
| Low-confidence | Khi AI không chắc, hệ thống có hỏi lại, show options hoặc chuyển người không? |
| Failure | Khi AI sai, user biết bằng cách nào và sửa thế nào? |
| Correction | Khi user sửa, correction có được lưu/log/học lại không hay biến mất? |

## 4. Viết finding thành quyết định

Không viết:

```text
Bot ngu, trả lời sai.
```

Viết:

```text
Khi user [trigger],
AI/product [failure],
hậu quả là [impact].
Lỗi thuộc layer [promise / intent / data-tool / safety / UX recovery].
Nên sửa bằng [requirement / UX / fallback / human role / test case].
```

Ví dụ:

```text
Khi user hỏi "chi tiêu linh tinh là gì?",
AI hiểu như keyword thay vì nhận ra intent mơ hồ,
hậu quả là user không biết sửa phân loại chi tiêu ở đâu.
Lỗi thuộc Intent + UX Recovery.
Nên sửa bằng low-confidence path: hỏi lại tiêu chí hoặc đưa 2-3 nhóm giao dịch để chọn.
```

## 5. Sketch as-is / to-be

Vẽ 2 cột:

- **As-is:** flow hiện tại, đánh dấu điểm gãy.
- **To-be:** flow đề xuất, đánh dấu path đã sửa.

Không cần đẹp. Cần nhìn vào là hiểu:

- user làm gì,
- AI làm gì,
- lúc AI không chắc thì sao,
- lúc AI sai user recover thế nào.

## 6. Tự kiểm trước khi nộp

- [ ] Có ít nhất 1 screenshot hoặc observation cụ thể.
- [ ] Có đủ 4 paths hoặc nói rõ path nào chưa có trong product.
- [ ] Finding được viết thành product decision, không chỉ là nhận xét.
- [ ] Sketch có as-is và to-be.
- [ ] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.

## Ví dụ điền: MoMo — Moni

### Product hứa gì?
- Trợ thủ tài chính cá nhân: phân tích chi tiêu, phân loại giao dịch, gợi ý tiết kiệm và cảnh báo chi tiêu bất thường.

### User nào được hứa sẽ được giúp?
- Người dùng cá nhân, thường xuyên giao dịch, cần nhìn tổng quan chi tiêu hàng tháng và phân loại nhanh các giao dịch lạ.

### Kỳ vọng của tôi khi dùng AI
- Gõ hoặc chọn giao dịch -> AI tự phân loại, đưa ra lý do/nhóm, và gợi ý hành động (ví dụ: đổi nhà cung cấp, tiết kiệm).

### Evidence (ví dụ minh họa)
- Screenshot: (chèn ảnh màn phân loại giao dịch) — placeholder.
- Prompt/input đã thử: "Phân loại giao dịch 23/05 - VnMart 235.000".
- Quan sát: AI gợi ý nhóm "Mua sắm" nhưng không cho lý do; không có tuỳ chọn sửa nhanh cho tất cả giao dịch tương tự.

### 4 paths

Happy:
- AI phân loại đúng, hiển thị confidence cao (ví dụ: 92%), có nút "Áp dụng cho 5 giao dịch tương tự". User thấy rõ lý do khi bấm vào "Chi tiết".

Low-confidence:
- AI hiển thị thông báo "Không chắc chắn" kèm 2-3 gợi ý nhóm để user chọn, hoặc nút "Hỏi lại".

Failure:
- AI phân loại sai (ví dụ: ghi là "Dịch vụ" thay vì "Mua sắm"). User chỉ biết khi review báo cáo tháng, không có cảnh báo trước.

Correction:
- Khi user sửa phân loại, hệ thống nên hiển thị checkbox "Áp dụng cho giao dịch tương tự" và lưu feedback để model/data pipeline học (hoặc ghi vào log cho rules engine).

### Finding (viết thành product decision)

Khi user review giao dịch (trigger), AI phân loại tự động nhưng không giải thích và không cung cấp cách sửa áp dụng hàng loạt (failure), hậu quả là user phải sửa thủ công nhiều giao dịch, gây friction và giảm trust (impact). Lỗi thuộc layers: intent/data-tool + UX recovery. Nên sửa bằng: hiển thị confidence, cung cấp 2-3 gợi ý nhóm khi low-confidence, và thêm action "Áp dụng cho N giao dịch tương tự" kèm logging feedback để pipeline học.

### As-is (flow hiện tại)
- App tự phân loại giao dịch khi import.
- Không hiển thị confidence hay lý do.
- User review cuối tháng, phát hiện sai -> sửa từng cái.

### To-be (flow đề xuất)
- Khi import/hiện giao dịch: show classification + confidence %.
- Nếu confidence < threshold: show 2-3 suggested groups and "Không chắc/Chọn nhóm".
- Khi user sửa: show "Áp dụng cho N giao dịch tương tự" và gửi feedback vào logs / lightweight rule update.

### SPEC change (1 câu)
- Thêm UI state `classification_confidence` và action `apply_to_similar_transactions`; cập nhật pipeline để log sửa người dùng làm feedback cho retraining / rules.

### Test case đề xuất
- Given: 10 giao dịch tương tự, AI phân loại 6/10 đúng. When user sửa 4 cái còn lại and ticks "Áp dụng cho N giao dịch tương tự", Then: những giao dịch tương tự được cập nhật trong 1 action and a feedback event is created.

### Checklist (đã bổ sung ví dụ)
- [x] Có ít nhất 1 screenshot hoặc observation cụ thể (placeholder).
- [x] Có đủ 4 paths.
- [x] Finding được viết thành product decision.
- [x] Sketch có as-is và to-be.
- [x] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.
