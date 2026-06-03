# Evidence Pack - Thin SPEC Day 05

Nộp kèm thin SPEC cuối Day 05.

## 1. Nhóm và track

**Tên nhóm:** Nhóm AI Agent / Personal Assistant  
**Track:** AI Agent / Personal Assistant  
**Product/app đã chọn:** Trợ lý AI lên lịch trình và cá nhân hóa trải nghiệm vui chơi tại VinWonders.  
**Build slice đang nghĩ:** Agent nhận ràng buộc thời gian + sở thích của đoàn khách, lọc các trò chơi/show phù hợp, trả về 1-3 option tốt nhất kèm thời gian dự kiến, và cảnh báo khi lịch quá sát hoặc ràng buộc mâu thuẫn.

## 2. Self-use evidence

Nhóm tự đặt mình vào workflow của khách đi công viên giải trí trong ngày: đọc thông tin trò chơi/show, tự ghép lịch theo khung giờ, và quyết định điểm đến tiếp theo.

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Khi phải tự đọc danh sách trò chơi, mô tả, khung giờ show và giờ đóng/mở cửa, người dùng nhanh bị quá tải vì phải vừa lọc sở thích, vừa tính thời gian di chuyển, vừa tránh trùng lịch. | Quan sát nội bộ từ workflow lập lịch; xem thêm pain statement trong `02-group-spec/thin-spec-template.md`. | Happy | Prototype không nên chỉ chat mở rộng. Cần bắt đầu bằng 3-4 input ngắn: giờ bắt đầu, giờ phải về, nhu cầu nghỉ/di chuyển, sở thích/đối tượng trong đoàn. |
| Các show/sự kiện có giờ cố định dễ bị bỏ lỡ nếu user đang ở khu vực xa hoặc đang chơi trò khác lâu hơn dự kiến. | Quan sát nội bộ từ SPEC: show có khung giờ vận hành cố định. | Failure | Agent phải cộng thêm buffer di chuyển/chờ đợi, không chỉ so sánh giờ bắt đầu - giờ kết thúc một cách máy móc. |
| Khi user hỏi quá chung chung như "có trò nào vui không?", hệ thống nếu trả lời một danh sách dài sẽ không giảm được việc phải tự chọn. | Giả lập prompt trong nhóm theo path Low-confidence. | Low-confidence | Khi thiếu constraint, AI nên hỏi lại 1-2 câu ngắn hoặc đưa nút chọn nhanh: có trẻ em không, thích cảm giác mạnh hay nhẹ, trong nhà hay ngoài trời. |
| Khi user đổi ý, ví dụ "thôi không chơi tàu lượn nữa", lịch trình cũ lập tức bị sai vì khoảng trống và thứ tự di chuyển thay đổi. | Giả lập correction flow trong Thin SPEC. | Correction | Prototype cần có thao tác xóa/sửa một mục đã chốt, sau đó tính lại quỹ thời gian trống và gợi ý option mới gần nhất. |

## 3. User / review / social evidence

Hiện tại nhóm chưa có review/quote trực tiếp từ khách VinWonders bên ngoài nhóm. Các dòng dưới là giả định có căn cứ từ trải nghiệm tương tự khi đi công viên giải trí, cần kiểm lại trước M1 Day 06.

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Đi theo gia đình/nhóm bạn thì mỗi người muốn một kiểu, mất thời gian đứng lại bàn xem chơi gì tiếp." | Giả định phỏng vấn nhanh trong nhóm / giả lập persona. | Khách đi theo đoàn, có nhiều sở thích khác nhau. | Decision friction: khó chốt điểm đến tiếp theo nếu chỉ có danh sách thông tin. |
| "Nếu sắp đến giờ show mà mình đang ở xa thì rất dễ lỡ, vì không ước lượng được phải đi mất bao lâu." | Giả định dựa trên self-use workflow. | Khách đi chơi trong ngày, có lịch show cố định. | Failure: lịch quá sát, bỏ qua thời gian di chuyển/xếp hàng. |
| "Chatbot mà hỏi dài quá thì lúc đang đi chơi sẽ lười gõ." | Giả định từ hành vi mobile-on-the-go. | Khách đang di chuyển, mệt, ưu tiên thao tác nhanh. | Low-confidence UX: cần câu hỏi ngắn, nút chọn nhanh, tránh bắt user mô tả dài. |

```text
Đây là giả định. Nhóm sẽ kiểm bằng phỏng vấn nhanh 2-3 bạn từng đi công viên giải trí/VinWonders và test 3 prompt mẫu trước checkpoint M1 Day 06:
1. "Nhà mình có trẻ em, còn 2 tiếng nữa, gợi ý chơi gì?"
2. "Có trò nào vui không?"
3. "Mình muốn xem show lúc 15:00 nhưng đang ở khu khác, có kịp không?"
```

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| Google Maps / itinerary planning | Gợi ý địa điểm gần bạn, ước lượng thời gian di chuyển và sắp xếp theo vị trí/thời gian. | Mỗi gợi ý lịch trình cần có travel-time buffer, không chỉ đưa ra tên địa điểm. | Có. Có thể hard-code buffer 10-15 phút/khu vực trong prototype. |
| TripIt / travel itinerary | Gom các mục lịch trình thành timeline, mỗi mục có giờ, địa điểm, trạng thái. | Nên hiện kết quả theo timeline để user tin được lịch có khả thi. | Có. UI có thể là danh sách timeline đơn giản. |
| Klook / travel activity booking | Lọc hoạt động theo sở thích, thời lượng, giá/lịch trong ngày. | Filter trước, chỉ hiện một số option tốt nhất thay vì đẩy toàn bộ catalog cho user. | Có. Prototype chỉ cần trả 1-3 option. |
| MoMo Moni teardown của Nguyễn Hoàng Long | Moni phân loại giao dịch đúng trong happy path nhưng thiếu low-confidence và correction loop khi AI sai. | AI không nên "tự tin mù quáng". Khi thiếu dữ liệu phải hỏi lại; khi user sửa phải cập nhật context. | Có. Thêm low-confidence question và correction path vào chat flow. |

## 5. Evidence -> Insight

```text
Evidence nổi bật nhất:
Người dùng không chỉ cần biết "có những trò/show nào", mà cần quyết định nhanh "bây giờ nên làm gì tiếp" trong điều kiện thời gian, vị trí, sở thích và sức lực có hạn.

Insight:
User không chỉ gặp vấn đề thiếu thông tin.
Thật ra họ cần decision support và recovery: lọc bớt thông tin, ước lượng tính khả thi, và sửa lịch nhanh khi đổi ý hoặc khi không kịp.

Opportunity:
AI có thể giúp bằng cách augmentation hẹp: hỏi constraint ngắn, lọc catalog, tính buffer thời gian, đưa 1-3 option khả thi, cảnh báo lịch quá sát, và để user quyết định cuối.
```

## 6. Evidence đổi SPEC như thế nào?

- [ ] Đổi user chính.
- [x] Đổi pain statement.
- [x] Đổi build slice.
- [ ] Đổi Auto/Aug decision.
- [x] Đổi 4 paths.
- [x] Đổi failure mode.
- [x] Đổi owner/test plan.

Ghi rõ 1-2 thay đổi quan trọng:

```text
Trước evidence, nhóm dễ bị nghĩ theo hướng "AI gợi ý trò chơi/show phù hợp" như một chatbot tư vấn chung.
Sau evidence, nhóm đổi thành "AI lập option lịch trình khả thi" với đầu vào ràng buộc thời gian, sở thích, buffer di chuyển và khả năng sửa lịch.
Lý do:
Pain lớn nhất không phải là không có thông tin, mà là quá tải khi phải tự ghép thông tin thành quyết định trong lúc đang đi chơi.

Trước evidence, failure mode chỉ là user đưa ràng buộc quá hẹp/mâu thuẫn.
Sau evidence, failure mode nguy hiểm nhất là AI bỏ qua thời gian di chuyển/xếp hàng và lưu một lịch nhìn có vẻ hợp lý nhưng thực tế không kịp.
Lý do:
Với công viên giải trí, sai 10-15 phút có thể làm user lỡ show cố định giờ hoặc phải di chuyển gấp, làm giảm trải nghiệm.
```
