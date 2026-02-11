import React from 'react';
import Markdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const slugify = (text) =>
    text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-');

const DocumentationViewer = ({ markdown }) => {
    return (
        <div className="prose prose-lg max-w-none">
            <Markdown
                components={{
                    h1({ children }) {
                        const id = slugify(children.toString());
                        return (
                            <h1 id={id} className="scroll-mt-32">
                                {children}
                            </h1>
                        );
                    },
                    h2({ children }) {
                        const id = slugify(children.toString());
                        return (
                            <h2 id={id} className="scroll-mt-32">
                                {children}
                            </h2>
                        );
                    },
                    h3({ children }) {
                        const id = slugify(children.toString());
                        return (
                            <h3 id={id} className="scroll-mt-32">
                                {children}
                            </h3>
                        );
                    },
                    code({ node, inline, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || '');
                        return !inline && match ? (
                            <SyntaxHighlighter
                                style={vscDarkPlus}
                                language={match[1]}
                                PreTag="div"
                                {...props}
                            >
                                {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                        ) : (
                            <code className={className} {...props}>
                                {children}
                            </code>
                        );
                    }
                }}
            >
                {markdown}
            </Markdown>
        </div>
    );
};

export default DocumentationViewer;
