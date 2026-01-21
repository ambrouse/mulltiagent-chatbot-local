import React from "react";
import styles from '../assets/css/HomePage.module.css' 
import { useNavigate } from 'react-router-dom';


function HomePage(){
    const navigate = useNavigate();



    const handleSelect = (featureId) => {
        navigate(`/${featureId}`);
    };
    const FEATURES = [
        {
        id: 'search',
        title: 'Tra Cứu Tài Liệu',
        desc: 'Tìm kiếm nhanh thông tin từ kho dữ liệu văn bản pháp luật.',
        icon: (
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        )
        },
        {
        id: 'contract',
        title: 'Tạo Hợp Đồng',
        desc: 'Tự động điền và soạn thảo hợp đồng dựa trên mẫu có sẵn.',
        icon: (
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16.5 2.5c1.104 0 2 .896 2 2v2.75a.75.75 0 0 1-1.5 0V4.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v16a.5.5 0 0 0 .5.5h6.25a.75.75 0 0 1 0 1.5H7a2 2 0 0 1-2-2v-16a2 2 0 0 1 2-2h9.5Z"/><path d="M14.5 14.5 19 19"/><path d="m19 14.5-4.5 4.5"/><path d="m13 19 3 3"/><path d="m16 22 3-3"/></svg>
        )
        },
        {
        id: 'ocr',
        title: 'Xử Lý Ảnh',
        desc: 'Quét OCR trích xuất thông tin từ giấy tờ và ảnh chụp.',
        icon: (
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
        )
        },
        {
        id: 'regulation',
        title: 'Đối Chiếu Điều Lệ',
        desc: 'So sánh văn bản hiện tại với quy chuẩn để tìm sai lệch.',
        icon: (
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>
        )
        }
    ];
return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Cổng Dịch Vụ Chatbot</h1>
        <p>Chọn tác vụ bạn muốn thực hiện</p>
      </header>

      <div className={styles.grid}>
        {FEATURES.map((feature) => (
          <div 
            key={feature.id} 
            className={styles.card}
            onClick={() => handleSelect(feature.id)}
          >
            <div className={styles.iconWrapper}>
              {feature.icon}
            </div>
            <h3>{feature.title}</h3>
            <p>{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
)
}


export default HomePage