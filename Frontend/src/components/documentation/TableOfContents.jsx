import React from 'react';

const slugify = (text) =>
    text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-');

const TableOfContents = ({ markdown }) => {
    if (!markdown) return null;

    const headings = markdown.match(/^#{1,3} .+$/gm) || [];

    return (
        <nav className="space-y-2">
            <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-widest mb-4">
                Table of Contents
            </h3>

            <ul className="space-y-2">
                {headings.map((heading, index) => {
                    const level = heading.match(/^#+/)[0].length;
                    const text = heading.replace(/^#+ /, '');
                    const id = slugify(text);

                    return (
                        <li
                            key={index}
                            style={{ paddingLeft: `${(level - 1) * 1.2}rem` }}
                        >
                            <a
                                href={`#${id}`}
                                className="block text-sm font-medium text-gray-800 hover:text-indigo-600 transition-colors duration-200"
                            >
                                {text}
                            </a>
                        </li>
                    );
                })}
            </ul>
        </nav>
    );
};

export default TableOfContents;
