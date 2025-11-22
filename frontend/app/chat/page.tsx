"use client"

import type React from "react"
import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Send } from "lucide-react"
import { AppLayout } from "@/components/app-layout"
import ReactMarkdown from "react-markdown"

interface Message {
  id: number
  text: string
  isBot: boolean
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async () => {
    const trimmed = inputValue.trim()
    if (!trimmed) return

    const userMessage: Message = {
      id: messages.length + 1,
      text: trimmed,
      isBot: false,
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    try {
      const res = await fetch("http://localhost:8000/chatbot/db-ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      })

      const data = await res.json()
      const botMessage: Message = {
        id: messages.length + 2,
        text: data.answer  || "No response from server.",
        isBot: true,
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: messages.length + 2,
          text: "Error contacting server.",
          isBot: true,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <AppLayout>
      <div className="flex flex-col h-[calc(100vh-73px)]">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.isBot ? "justify-start" : "justify-end"}`}>
                <div
                  className={`px-4 py-2 rounded-2xl ${
                    message.isBot
                      ? "bg-red-700/50 text-white border border-red-600/30 max-w-3xl w-full"
                      : "bg-gradient-to-b from-black to-red-900/80 text-white border border-white/20 max-w-md"
                  }`}
                >
                {message.isBot ? (
                  <div className="prose prose-invert text-sm max-w-none">
                    <ReactMarkdown>{message.text}</ReactMarkdown>
                  </div>
                ) : (
                  <p className="text-sm">{message.text}</p>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="text-sm text-white/70 italic">Bot is typing...</div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Chat Input */}
        <div className="p-4 border-t border-white/10">
          <div className="flex items-center space-x-2 bg-black/20 rounded-full p-2 border border-white/20">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask chatbot"
              className="flex-1 bg-transparent border-none text-white placeholder-white/60 focus:ring-0 focus:outline-none"
            />
            <Button
              onClick={handleSendMessage}
              size="icon"
              className="bg-red-600 hover:bg-red-700 text-white rounded-full h-8 w-8"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
