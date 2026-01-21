import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';

const BotMessage = ({ content }) => {
  return (
    // Class này giúp reset CSS mặc định để Markdown hiển thị đúng
    <div className="markdown-body" style={{backgroundColor: 'transparent', fontSize: 'inherit'}}> 
      <ReactMarkdown
        children={content}
        remarkPlugins={[remarkGfm]}
        components={{
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <SyntaxHighlighter
                style={dracula}
                language={match[1]}
                PreTag="div"
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code className={className} {...props} style={{background: '#eee', padding: '2px 4px', borderRadius: '4px'}}>
                {children}
              </code>
            );
          },
          // Style cho thẻ table nếu cần
          table({children}) {
             return <table style={{borderCollapse: 'collapse', width: '100%', margin: '10px 0'}}>{children}</table>
          },
          th({children}) {
             return <th style={{border: '1px solid #ddd', padding: '8px', background: '#f2f2f2'}}>{children}</th>
          },
          td({children}) {
             return <td style={{border: '1px solid #ddd', padding: '8px'}}>{children}</td>
          }
        }}
      />
    </div>
  );
};

export default BotMessage;