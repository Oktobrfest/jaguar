import React, { useState, useEffect } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const AiAnswer = ({ aiResponse }) => {
    const [ aiAnswer, setAiAnswer ] = useState(aiResponse);

    useEffect(() => {
        setAiAnswer(aiResponse);
    }, [ aiResponse ]);

    const renderCode = (code) => {
        // Extract the language and the actual code content from the formatted code block
        const regex = /```(\w+)\n([\s\S]+?)```/;
        const match = regex.exec(code);
        const language = match ? match[1].toLowerCase() : 'plaintext';
        const actualCode = match ? match[2] : code;


        return (
            <SyntaxHighlighter language={ language } style={ dark }>
                { actualCode }
            </SyntaxHighlighter>
        );
    };

    const renderAnswerSet = (answerSet, title) => (
        <div className="answer-set">
            <div className="title-and-only-answer">
                <h4>{ title }</h4>
                { answerSet['ONLY ANSWER'] && <div><strong>Answer:</strong> { answerSet['ONLY ANSWER'] }</div> }
            </div>
            { answerSet['SHORT ANSWER'] && <div><strong>Short Answer:</strong> { answerSet['SHORT ANSWER'] }</div> }
            { answerSet['CODE'] && <div>{ renderCode(answerSet['CODE']) }</div> }
            { answerSet['ELABORATION'] && <div>{ answerSet['ELABORATION'] }</div> }
        </div>
    );


    return (
        <div id="ai-answer-container">
            { aiAnswer && (
                <>
                    { aiAnswer.gpt && renderAnswerSet(aiAnswer.gpt, "GPT") }
                    { aiAnswer.google && renderAnswerSet(aiAnswer.google, "Google") }
                </>
            ) }
        </div>
    );
};

export default AiAnswer;
