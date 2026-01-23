import React, { useState } from 'react';
import type { Citation } from '../citation.types';
import { BookOpen } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import '../citation.css';

interface Props {
    text: string;
    citations: Record<string, Citation> | null;
}

export const CitationRenderer: React.FC<Props> = ({ text, citations }) => {
    const [hoveredCitation, setHoveredCitation] = useState<Citation | null>(null);

    // Regex to match [C1], [C2], etc.
    const parts = text.split(/(\[C\d+\])/g);

    return (
        <div className="citation-text">
            {parts.map((part, i) => {
                const match = part.match(/^\[(C\d+)\]$/);
                if (match) {
                    const cid = match[1];
                    const citation = citations?.[cid];

                    if (!citation) return <span key={i} className="citation-missing">{part}</span>;

                    return (
                        <span key={i} className="citation-wrapper">
                            <button
                                onMouseEnter={() => setHoveredCitation(citation)}
                                onMouseLeave={() => setHoveredCitation(null)}
                                className="citation-badge"
                            >
                                {cid}
                            </button>

                            <AnimatePresence>
                                {hoveredCitation?.id === cid && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                                        animate={{ opacity: 1, y: 0, scale: 1 }}
                                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                                        className="citation-tooltip"
                                    >
                                        <div className="citation-header">
                                            <BookOpen size={12} />
                                            <span>Source: {citation.source} • Page {citation.page}</span>
                                        </div>
                                        <p className="citation-snippet">
                                            "{citation.snippet}"
                                        </p>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </span>
                    );
                }
                return <span key={i}>{part}</span>;
            })}
        </div>
    );
};
