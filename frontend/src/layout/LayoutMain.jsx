import React, { useEffect, useRef, useState } from 'react';
import { Outlet, Link } from 'react-router-dom';
import styles from '../assets/css/LayoutMain.module.css'
import { useNavigate } from 'react-router-dom';

function LayoutMain(){
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);
    const navigate = useNavigate();

    // Toggle bật tắt menu
    const toggleMenu = () => setIsOpen(!isOpen);

    // Logic: Click ra ngoài thì đóng menu
    useEffect(() => {
        const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setIsOpen(false);
        }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    
    return(
        <>
            <header>
                <nav className={styles.navbarContainer} ref={dropdownRef}>
                    {/* Nút bấm chính */}
                    <button 
                        className={styles.menuBtn} 
                        onClick={toggleMenu}
                        aria-expanded={isOpen}
                    >
                        {/* Icon Hamburger (SVG) */}
                        <svg 
                            width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                        >
                            {isOpen ? (
                                <path d="M18 6L6 18M6 6l12 12" /> // Dấu X
                            ) : (
                                <path d="M3 12h18M3 6h18M3 18h18" /> // 3 gạch ngang
                            )}
                        </svg>
                        <span>Menu</span>
                    </button>

                    {/* Dropdown Menu */}
                    <div className={`${styles.dropdown} ${isOpen ? styles.active : ''}`}>
                        <div className={styles.menuItem}
                            onClick={()=>{
                                navigate("/");
                            }}
                        >
                            <span className={styles.iconWrapper}>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                                </svg>
                            </span> 
                            Trang chủ
                        </div>

                        {/* 2. Tra Cứu Tài Liệu (Icon Kính lúp soi văn bản) */}
                        <div className={styles.menuItem}>
                            <span className={styles.iconWrapper}>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14 2 14 8 20 8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                    <polyline points="10 9 9 9 8 9"></polyline>
                                </svg>
                            </span> 
                            Tra Cứu Tài Liệu
                        </div>

                        {/* 3. Tạo Hợp Đồng (Icon Cây bút viết lên giấy) */}
                        <div className={styles.menuItem}
                            onClick={()=>{
                                navigate("/contract");
                            }}
                        >
                            <span className={styles.iconWrapper}>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                                </svg>
                            </span> 
                            Tạo Hợp Đồng
                        </div>

                        {/* 4. Xử Lý Ảnh (Icon Quét/Scan tài liệu) */}
                        <div className={styles.menuItem}>
                            <span className={styles.iconWrapper}>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M21 12V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h7"></path>
                                    <circle cx="12" cy="12" r="3"></circle> {/* Ống kính */}
                                    <path d="M17 17l4 4m0-4l-4 4"></path> {/* Ký hiệu xử lý */}
                                </svg>
                            </span> 
                            Xử Lý Ảnh (OCR)
                        </div>

                        {/* 5. Đối Chiếu Điều Lệ (Icon Cái cân công lý) */}
                        <div className={styles.menuItem}>
                            <span className={styles.iconWrapper}>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M12 3v19"></path> {/* Trục giữa */}
                                    <path d="M6 6h12"></path>  {/* Cán cân ngang */}
                                    <path d="M6 6L3 13h6L6 6z"></path> {/* Đĩa cân trái */}
                                    <path d="M18 6l-3 7h6l-3-7z"></path> {/* Đĩa cân phải */}
                                </svg>
                            </span> 
                            Đối Chiếu Điều Lệ
                        </div>
                        
                        {/* <div className={styles.divider}></div> */}
                        
                        {/* <div className={styles.menuItem} style={{color: '#ef4444'}}>
                            <span>🚪</span> Đăng xuất
                        </div> */}
                    </div>
                    </nav>
            </header>
            <main>
                <Outlet />
            </main>
            {/* <footer>
                <div className={styles.footer}>
                    <p>footer</p>
                </div>
            </footer> */}
        </>

    )
}

export default LayoutMain;