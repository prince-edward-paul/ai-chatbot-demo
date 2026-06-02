interface Props {
    setFile: (file: File | null) => void;
    uploadPdf: () => void;
    loading: boolean;
  }
  
  export default function UploadBox({
    setFile,
    uploadPdf,
    loading
  }: Props) {
  
    return (
      <div style={{ marginBottom: "30px" }}>
  
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            if (e.target.files) {
              setFile(e.target.files[0]);
            }
          }}
        />
  
        <br /><br />
  
        <button
          onClick={uploadPdf}
          style={{
            padding: "10px 20px",
            backgroundColor: "blue",
            color: "white",
            border: "none",
            cursor: "pointer"
          }}
        >
          {loading ? "Analyzing..." : "Upload PDF"}
        </button>
  
      </div>
    );
  }