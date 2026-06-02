"use client";

import { useState } from "react";
import axios from "axios";

import Header from "../components/Header";
import UploadBox from "../components/UploadBox";
import ChatBox from "../components/ChatBox";
import MessageBubble from "../components/MessageBubble";

interface Message {
  role: string;
  content: string;
}

export default function Home() {

  const [file, setFile] = useState<File | null>(null);

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<Message[]>([]);

  const simulateStreaming = async (
    fullText: string
  ) => {

    let currentText = "";

    const aiMessageIndex = messages.length + 1;

    setMessages((prev) => [
      ...prev,
      {
        role: "ai",
        content: ""
      }
    ]);

    const words = fullText.split(" ");

    for (let i = 0; i < words.length; i++) {

      currentText += words[i] + " ";

      await new Promise((resolve) =>
        setTimeout(resolve, 30)
      );

      setMessages((prev) => {

        const updated = [...prev];

        updated[aiMessageIndex] = {
          role: "ai",
          content: currentText
        };

        return updated;
      });
    }
  };

  const uploadPdf = async () => {

    if (!file) {
      alert("Select a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/upload-pdf",
        formData
      );

      await simulateStreaming(
        res.data.analysis
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  const askQuestion = async () => {

    if (!question) return;

    const userMessage = {
      role: "user",
      content: question
    };

    setMessages((prev) => [
      ...prev,
      userMessage
    ]);

    const currentQuestion = question;

    setQuestion("");

    try {

      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/ask-pdf",
        {
          question: currentQuestion
        }
      );

      await simulateStreaming(
        res.data.answer
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  return (
    <main className="min-h-screen bg-slate-900 text-white">
      <div className="max-w-4xl mx-auto p-6">

        <Header />

        <div className="bg-slate-800 p-6 rounded-3xl shadow-2xl">

          <UploadBox
            setFile={setFile}
            uploadPdf={uploadPdf}
            loading={loading}
          />

          <ChatBox
            question={question}
            setQuestion={setQuestion}
            askQuestion={askQuestion}
            loading={loading}
          />

          <div className="mt-8">

            {messages.map((message, index) => (
              <MessageBubble
                key={index}
                role={message.role}
                content={message.content}
              />
            ))}

            {loading && (
              <div className="mt-4 text-gray-400">
                AI is thinking...
              </div>
            )}

          </div>

        </div>

      </div>
    </main>
  );
}