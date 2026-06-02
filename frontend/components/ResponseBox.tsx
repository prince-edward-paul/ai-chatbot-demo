interface Props {
    response: string;
  }
  
  export default function ResponseBox({
    response
  }: Props) {
  
    return (
      <div
        style={{
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "10px",
          minHeight: "200px"
        }}
      >
        <h2>AI Response</h2>
  
        <p style={{ whiteSpace: "pre-wrap" }}>
          {response || "AI response will appear here"}
        </p>
  
      </div>
    );
  }