interface Props {
    role: string;
    content: string;
  }
  
  export default function MessageBubble({
    role,
    content
  }: Props) {
  
    const isUser = role === "user";
  
    return (
      <div
        className={`flex mb-4 ${
          isUser
            ? "justify-end"
            : "justify-start"
        }`}
      >
  
        <div
          className={`max-w-[75%] p-4 rounded-2xl shadow-lg whitespace-pre-wrap ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-gray-800 text-gray-100"
          }`}
        >
  
          <div className="font-bold mb-2">
            {isUser ? "You" : "AI"}
          </div>
  
          {content}
  
        </div>
  
      </div>
    );
  }