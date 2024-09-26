import React, { useState, useEffect, ChangeEvent } from "react";

// Define types for the prompt
interface Prompt {
    prompt_id: number;
    prompt_text: string;
}

function SettingsPage() {
    // State for prompts and new prompt text
    const [prompts, setPrompts] = useState<Prompt[]>([]);
    const [newPromptText, setNewPromptText] = useState<string>('');

    // Fetch prompts on component load
    useEffect(() => {
        fetch('/prompts')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data: Prompt[]) => {
                setPrompts(data);
            })
            .catch(error => {
                console.error('Error fetching prompts:', error);
            });
    }, []);

    // Handle update of an existing prompt
    const handleUpdate = (promptId: number, updatedText: string) => {
        fetch(`/prompts/${promptId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt_text: updatedText }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error updating prompt');
            }
            setPrompts(prompts.map(prompt =>
                prompt.prompt_id === promptId ? { ...prompt, prompt_text: updatedText } : prompt
            ));
        })
        .catch(error => {
            console.error('Error updating prompt:', error);
        });
    };

    // Handle creation of a new prompt
    const handleCreate = () => {
        fetch('/prompts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt_text: newPromptText }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error creating prompt');
            }
            return response.json();
        })
        .then((newPrompt: Prompt) => {
            setPrompts([...prompts, newPrompt]);
            setNewPromptText('');  // Clear input after creation
        })
        .catch(error => {
            console.error('Error creating prompt:', error);
        });
    };

    // Handle text change in input fields
    const handleChange = (e: ChangeEvent<HTMLInputElement>, promptId: number) => {
        const updatedText = e.target.value;
        handleUpdate(promptId, updatedText);
    };

    return (
        <div>
            <h1>Manage Prompts</h1>
            <ul>
                {prompts.map(prompt => (
                    <li key={prompt.prompt_id}>
                        <input
                            type="text"
                            value={prompt.prompt_text}
                            onChange={(e) => handleChange(e, prompt.prompt_id)}
                        />
                    </li>
                ))}
            </ul>
            <div>
                <input
                    type="text"
                    value={newPromptText}
                    onChange={(e) => setNewPromptText(e.target.value)}
                />
                <button onClick={handleCreate}>Create New Prompt</button>
            </div>
        </div>
    );
}

export { SettingsPage };
