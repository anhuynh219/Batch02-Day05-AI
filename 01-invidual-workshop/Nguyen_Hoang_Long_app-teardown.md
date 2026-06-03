# Workshop — Mổ App AI Thật: Phân tích MoMo Moni

## 1. Chọn một sản phẩm để dùng thử

* **Sản phẩm được chọn:** MoMo — Moni (Trợ thủ tài chính)
* **AI feature:** Trợ thủ tài chính, phân tích chi tiêu, chatbot AI.
* **Cách truy cập:** Icon "Moni" hoặc "Quản lý chi tiêu" trên màn hình chính của App MoMo.

## 2. Dùng thử: promise vs reality

* **Product hứa gì?** Giúp người dùng thảnh thơi quản lý tiền bạc, tự động phân tích và nhắc nhở chi tiêu thông minh bằng AI chatbot.
* **User nào được hứa sẽ được giúp?** Người dùng MoMo thường xuyên giao dịch thanh toán, chuyển tiền nhưng lười ghi chép sổ sách thủ công.
* **Bạn kỳ vọng AI làm được task nào?** Nhận diện chính xác ngữ cảnh của các khoản chuyển tiền cá nhân (Peer-to-peer) dựa trên nội dung chuyển khoản (ví dụ: "tien an trua", "tra tien cafe") để đưa vào đúng danh mục báo cáo chi tiêu, thay vì chỉ gom hết vào "Chuyển tiền".
* **Khi dùng thật, điểm gãy xuất hiện ở đâu?** AI phân loại cực tốt với các giao dịch quét mã QR tại cửa hàng (ví dụ: QR Highlands Coffee -> Ăn uống). Tuy nhiên, gãy ở các giao dịch chuyển tiền cá nhân dù nội dung chuyển khoản có chứa từ khóa rõ ràng.

**Evidence:**
* **Prompt/Input đã thử:** Chuyển 50.000đ cho bạn bè với nội dung "Tra tien an trua". Sau đó hỏi Moni: *"Tháng này tôi tiêu bao nhiêu cho ăn uống rồi?"*
* **Hành vi quan sát được:** Moni đưa ra con số báo cáo **không bao gồm** khoản 50.000đ kia. Khoản đó bị vứt vào danh mục "Chuyển tiền/Rút tiền" (không tính vào chi tiêu).
* **Quote/Screenshot (Mô phỏng):** Pie chart báo cáo chi tiêu hiển thị sai lệch thực tế. User phải vào lịch sử, bấm sửa tay từng giao dịch chuyển tiền thành "Ăn uống".

## 3. Vẽ 4 paths

| Path | Câu hỏi cần trả lời | Tình trạng trong App |
|---|---|---|
| **Happy** | Khi AI đúng và tự tin, user thấy gì? | User thanh toán hóa đơn điện/nước hoặc quét mã QR quán ăn. Moni tự động cộng đúng số tiền vào danh mục "Hóa đơn" hoặc "Ăn uống" và hiển thị biểu đồ tròn đẹp mắt. |
| **Low-confidence** | Khi AI không chắc, hệ thống có hỏi lại, show options hoặc chuyển người không? | *(Path này đang thiếu)* AI của Moni hiện tại đang tự tin một cách mù quáng. Nó thà phân loại sai (gom vào "Giao dịch khác/Chuyển tiền") chứ không có luồng hỏi lại user: *"Giao dịch này là ăn uống hay mua sắm?"* |
| **Failure** | Khi AI sai, user biết bằng cách nào và sửa thế nào? | User chỉ phát hiện sai khi thấy tổng tiền ăn uống báo cáo thấp bất thường. Sửa bằng cách: Vào lịch sử -> Chọn giao dịch -> Đổi danh mục thủ công. Quá trình này rườm rà. |
| **Correction** | Khi user sửa, correction có được lưu/log/học lại không hay biến mất? | Dường như biến mất với các giao dịch tương lai. Lần sau chuyển khoản với nội dung tương tự cho cùng một người, hệ thống vẫn tiếp tục phân loại sai thành "Chuyển tiền". |

## 4. Viết finding thành quyết định

**Finding 1: Phân loại sai giao dịch cá nhân**
> Khi user **[chuyển tiền cho cá nhân có kèm nội dung chỉ định chi tiêu (ví dụ: ăn trưa, cafe)]**, 
> AI/product **[không nhận diện được intent chi tiêu mà chỉ mặc định là giao dịch luân chuyển dòng tiền]**, 
> hậu quả là **[báo cáo tài chính sai lệch, khiến user mất niềm tin vào tính năng tự động và phải làm thủ công, làm mất đi "promise" ban đầu]**.
> Lỗi thuộc layer **[Intent + Data-tool]**. 
> Nên sửa bằng **[UX Recovery (Low-confidence path)]**: Bổ sung trigger quét từ khóa (regex cơ bản) trong nội dung chuyển tiền. Nếu có từ khóa nghi ngờ (ăn, cf, mua...), gửi một smart-suggestion card ngay trong box chat của Moni để user tap chọn xác nhận 1 chạm, thay vì phải vào sâu trong setting để sửa.

**Finding 2: Thiếu tính học hỏi (No continual learning)**
> Khi user **[sửa thủ công danh mục của một giao dịch]**, 
> AI/product **[không lưu logic này cho các giao dịch tương lai với cùng người nhận/nội dung]**, 
> hậu quả là **[user phải sửa đi sửa lại một lỗi nhiều lần]**.
> Lỗi thuộc layer **[Safety / Data-tool (chưa cá nhân hóa context)]**. 
> Nên sửa bằng **[Requirement]**: Lưu rule mapping cục bộ (local cache/user profile) "Người nhận A + Keyword B = Danh mục C" để tự động áp dụng hoặc gợi ý cho lần sau.

## 5. Sketch as-is / to-be

**[AS-IS FLOW] - Điểm gãy ở việc AI tự quyết định sai**
```text
(1) User chuyển 50k cho "Nguyen Van A" nội dung "tra tien cafe" 
   ↓
(2) AI quét giao dịch 
   ↓
(3) AI tự tin gán nhãn: [Danh mục: Chuyển tiền] ❌ (ĐIỂM GÃY: Tự tin mù quáng)
   ↓
(4) User hỏi Moni: "Tổng tiền cafe?"
   ↓
(5) AI trả về kết quả sai ❌
   ↓
(6) User bực mình -> Vào lịch sử -> Sửa tay. 
```

**[TO-BE FLOW] - Thêm Low-confidence path và Correction loop**
```text
(1) User chuyển 50k cho "Nguyen Van A" nội dung "tra tien cafe"
   ↓
(2) AI quét giao dịch. Nhận thấy "Người nhận cá nhân" + "Keyword: cafe"
   ↓
(3) AI không tự tin gán nhãn. Gán tạm [Danh mục: Chưa phân loại]
   ↓
(4) Moni chủ động gửi Smart-card trong chat/Notification: 
    "Khoản 50k cho Nguyen Van A là tiền Ăn uống hay Mua sắm?"
    [Nút: Ăn uống]  [Nút: Mua sắm]  [Nút: Chuyển tiền] ✅ (SỬA LỖI BẰNG UX)
   ↓
(5) User tap chọn [Ăn uống]. 
   ↓
(6) AI cập nhật báo cáo và LƯU RULE (Học lại cho lần sau). ✅ (CORRECTION PATH)
```

## 6. Tự kiểm trước khi nộp

- [x] Có ít nhất 1 screenshot hoặc observation cụ thể. *(Đã mô tả observation chi tiết trong phần 2).*
- [x] Có đủ 4 paths hoặc nói rõ path nào chưa có trong product. *(Đã chỉ rõ Low-confidence path đang bị thiếu).*
- [x] Finding được viết thành product decision, không chỉ là nhận xét.
- [x] Sketch có as-is và to-be. *(Được mô tả bằng text flow rõ ràng).*
- [x] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.
      -> **Câu chốt thay đổi SPEC:** *"Cập nhật SPEC module Nhận diện Giao dịch: Thêm luồng (flow) xác nhận danh mục 1-chạm (Smart-suggestion UI) dành riêng cho các giao dịch P2P có chứa từ khóa chi tiêu, và bổ sung cờ (flag) 'ghi nhớ lựa chọn' vào database cá nhân hóa của người dùng."*