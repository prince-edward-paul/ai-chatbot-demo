interface Props {
  question: string;
  setQuestion: (value: string) => void;
  askQuestion: () => void;
  loading: boolean;
}

export default function ChatBox({
  question,
  setQuestion,
  askQuestion,
  loading
}: Props) {

  return (
    <div className="mt-8">

      <h2 className="text-2xl font-bold mb-4">
        Chat With PDF
      </h2>

      <div className="flex gap-3">

        <input
          type="text"
          placeholder="Ask something about the PDF..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          className="flex-1 p-4 rounded-xl bg-gray-800 border border-gray-700 text-white"
        />

        <button
          onClick={askQuestion}
          className="bg-blue-600 hover:bg-blue-700 px-6 rounded-xl font-semibold"
        >
          {loading
            ? "Thinking..."
            : "Ask AI"}
        </button>

      </div>

    </div>
  );
}