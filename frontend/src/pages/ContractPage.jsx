import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from 'react-router-dom';
import styles from '../assets/css/ContractPage.module.css'
import {LoadTemplateHome, UploadTemplate, CreateFile, load_history, delete_template, load_session, delete_session} from '../services/ContractService'
import BotMessage from '../component/BotMessage'

function Contract(){
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [templateName,setTemplateName] = useState([])
  const [template, setTemplate] = useState(["",-1])
  const [inputUser, setInputUser] = useState("")
  const [history, setHistory] = useState([])
  const messagesEndRef = useRef(null);
  const [session, setSession] = useState([-1, -1])
  const [sessionList, setSessionList] = useState([])
  const navigate = useNavigate();

  const scrollToBottom = () => {
    // behavior: "smooth" giúp cuộn mượt mà thay vì nhảy bụp phát
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [history]);

  useEffect(()=>{
    LoadTemplateHome().then((data)=>{
      setTemplateName(data)
    })
    load_history(0,session[0]).then((data)=>{
      setHistory(data)
    })
    load_session().then((data)=>{
      setSessionList(data)
    })
  },[])

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };
    // console.log(history, session)
    
    
    return (
    <div className={styles.container}>
      {/* Overlay đen mờ khi mở menu trên mobile */}
      <div 
        className={`${styles.overlay} ${isSidebarOpen ? styles.active : ''}`} 
        onClick={()=>{
            toggleSidebar()
        }}
      ></div>

      {/* SIDEBAR */}
      {/* Kết hợp nhiều class: styles.sidebar VÀ styles.active nếu state true */}
      <aside className={`${styles.sidebar} ${isSidebarOpen ? styles.active : ''}`}>
        <div className={styles.sidebarHeader}
          onClick={()=>{
            navigate("/");
          }}
        >
          <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="24" width="24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5Z"></path>
            <path d="M8.5 8.5v.01"></path>
            <path d="M16 16v.01"></path>
            <path d="M12 12v.01"></path>
          </svg>
          <span>Contract GPT</span>
          
          {/* Nút đóng trên mobile */}
          <button 
            onClick={()=>{
                toggleSidebar()
            }} 
            style={{ marginLeft: 'auto', background: 'none', border: 'none', color: 'white', cursor: 'pointer' }} 
            className="md:hidden" 
          >
             <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>

        <button className={styles.uploadBtn}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="16"></line>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
          Tải lên Template mới
          <input 
            onChange={(e)=>{
              UploadTemplate(e.target.files[0]).then((data)=>{
                LoadTemplateHome().then((data)=>{
                  setTemplateName(data)
                })
              })

            }}
          type="file" />
        </button>

        <div className={styles.sectionTitle}>File đã tải lên</div>

        {/* LIST SCROLL NGANG */}
        <div className={styles.templateList}>
          <div className={styles.templateListInner}>
            {
              templateName.map((data, index)=>(
                <div key={index} className={`${styles.templateItem} ${template[1]==index ? styles.templateItem__active : ''}`}
                  onClick={()=>{
                    setTemplate([data, index])
                  }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                  <p>{data}</p>
                  <p
                    onClick={()=>{
                      delete_template(data).then((data_)=>{
                        LoadTemplateHome().then((data__)=>{
                          setTemplateName(data__)
                          alert("Đã xóa template: "+data)
                          if(template[1]==index){
                            setTemplate(["",-1])
                          }
                        })
                      })
                    }}
                  >xóa</p>  
                </div>
                
              ))}
          </div>
        </div>
        <div className={styles.sectionTitle}>Session</div>

        {/* LIST SCROLL NGANG */}
        <div className={styles.templateList}>
          <div className={styles.templateListInner}>
            {
              sessionList.map((data, index)=>(
                <div key={index} className={`${styles.templateItem} ${session[1]==index ? styles.templateItem__active : ''}`}
                  onClick={()=>{
                    setSession([data, index])
                    load_history(0,data).then((data_)=>{
                      setHistory(data_)
                    })
                  }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  <p>{data}</p>
                  <p
                    onClick={()=>{
                      delete_session(data).then((data_)=>{
                        load_session().then((data__)=>{
                          setSessionList(data__)
                          setSession([-1,-1])
                        })
                      })
                    }}
                  >xóa</p>  
                </div>
              ))}
          </div>
        </div>
        

        <div className={styles.userProfile}>
          {/* <div className={styles.avatar}>U</div> */}
          {/* <div style={{ fontSize: '0.9rem', fontWeight: 500 }}>User Admin</div> */}
        </div>
      </aside>

      {/* MAIN CHAT */}
      <main className={styles.mainChat}>
        {/* Header Mobile */}
        <div className={styles.mobileHeader}>
          <button onClick={toggleSidebar} style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
          </button>
          <span style={{ fontWeight: 'bold' }}>Contract GPT</span>
          <div style={{ width: '24px' }}></div>
        </div>

        <div className={styles.chatContainer}>
          {
            history?.map((data, index)=>{
              if(data.role=="user"){
                return(
                <div key={index} className={`${styles.message} ${styles.messageUser}`}>
                  <div className={styles.messageContent}>
                    <BotMessage content={data.mess} />
                  </div>
                </div>)
                // return (<p key={index} >User</p>)
              }else{
                return(
                <div key={index} className={`${styles.message} ${styles.messageBot}`}>
                  <div className={`${styles.iconAvatar} ${styles.botIcon}`}>
                    <svg stroke="white" fill="none" strokeWidth="2" viewBox="0 0 24 24" width="16" height="16" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5Z"></path></svg>
                  </div>
                  <div className={styles.messageContent}>
                    <BotMessage content={data.mess} />
                  </div>
                </div>)
                // return (<p key={index} >AI</p>)
              }

            })
          }
          <div ref={messagesEndRef} />


          {/* Bot Message */}

          {/* User Message */}
        </div>

        {/* Input Area */}
        <div className={styles.inputArea}>
          <div className={styles.inputWrapper}>
            <textarea 
              className={styles.textArea} 
              placeholder="Nhập tin nhắn vào đây..."
              value={inputUser}
              onChange={(e)=>{
                setInputUser(e.target.value)
              }}
            ></textarea>
            <button className={styles.sendBtn}
              onClick={()=>{
                if(template[0]==""){
                    alert("- Chưa chọn template!")
                    return 
                }
                if(inputUser==""){
                    alert("- Không được để  rỗng input!")
                    return 
                }
                const newItem = {"mess":inputUser,
                  "role":"user",
                  "id_user":"1",
                  "id_session":session[0]
                };
                setHistory(prev => [...prev, newItem]);
                setInputUser("")
                CreateFile(template[0], inputUser, session[0]).then((data)=>{
                    load_history(0,data.session).then((data_)=>{
                      setHistory(data_)
                      setSession([data.session, -1])
                      load_session().then((data__)=>{
                        setSessionList(data__)
                      })
                    })
                })
              }}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </div>
          <p className={styles.footerText}>ChatGPT có thể mắc lỗi. Hãy kiểm tra lại thông tin quan trọng.</p>
        </div>
      </main>
    </div>
  );
};

export default Contract;