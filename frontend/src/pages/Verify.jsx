import {
  useRef,
  useState
} from "react";

import {
  Upload,
  ShieldCheck,
  Image as ImageIcon,
  Sparkles
} from "lucide-react";

import API from "../api";

import Header
  from "../components/Header";


export default function Verify() {

  const inputRef =
    useRef(null);


  const [
    file,
    setFile
  ] = useState(null);

  const [
    preview,
    setPreview
  ] = useState("");

  const [
    result,
    setResult
  ] = useState(null);

  const [
    loading,
    setLoading
  ] = useState(false);

  const [
    dragging,
    setDragging
  ] = useState(false);

  const [
    error,
    setError
  ] = useState("");


  const selectFile =
    selected => {

      setError("");
      setResult(null);

      if (!selected) return;

      if (
        !selected.type.startsWith(
          "image/"
        )
      ) {

        setError(
          "Please select an image."
        );

        return;
      }

      if (
        selected.size >
        10 * 1024 * 1024
      ) {

        setError(
          "Maximum image size is 10 MB."
        );

        return;
      }

      if (preview) {
        URL.revokeObjectURL(
          preview
        );
      }

      setFile(
        selected
      );

      setPreview(
        URL.createObjectURL(
          selected
        )
      );
    };


  const verify =
    async () => {

      if (!file) {

        setError(
          "Please select a signature image."
        );

        return;
      }

      setLoading(true);
      setError("");
      setResult(null);

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      try {

        const response =
          await API.post(
            "/verification/",
            formData,
            {
              headers: {
                "Content-Type":
                  "multipart/form-data"
              }
            }
          );

        setResult(
          response.data.verification
        );

      } catch (err) {

        setError(
          err.response?.data?.error ||
          "Verification failed."
        );

      } finally {

        setLoading(false);

      }
    };


  const clear =
    () => {

      setFile(null);
      setPreview("");
      setResult(null);
      setError("");

      if (
        inputRef.current
      ) {
        inputRef.current.value =
          "";
      }
    };


  const genuine =
    result?.result ===
    "Genuine";


  return (
    <>
      <Header
        title="Verify Signature"
      />


      <div className="page">

        <div className="page-heading">

          <div>

            <span className="eyebrow">
              AI VERIFICATION
            </span>

            <h2>
              Analyze a signature
            </h2>

            <p>
              Upload a signature image
              and get an AI-powered
              authenticity decision.
            </p>

          </div>

        </div>


        <div className="verify-grid">

          <div className="dashboard-card">

            <div className="card-heading">

              <div>

                <h3>
                  Upload signature
                </h3>

                <p>
                  PNG, JPG, JPEG or WEBP
                  · Maximum 10 MB
                </p>

              </div>

            </div>


            <div
              className={`upload-box ${
                dragging
                  ? "dragging"
                  : ""
              } ${
                file
                  ? "selected"
                  : ""
              }`}
              onDragOver={e => {

                e.preventDefault();

                setDragging(
                  true
                );
              }}
              onDragLeave={() =>
                setDragging(
                  false
                )
              }
              onDrop={e => {

                e.preventDefault();

                setDragging(
                  false
                );

                selectFile(
                  e.dataTransfer.files?.[0]
                );
              }}
              onClick={() =>
                inputRef.current?.click()
              }
            >

              <input
                ref={inputRef}
                type="file"
                accept="image/*"
                hidden
                onChange={e =>
                  selectFile(
                    e.target.files?.[0]
                  )
                }
              />


              {preview ? (

                <div className="preview">

                  <div className="preview-image">
                    <img
                      src={preview}
                      alt="Signature"
                    />
                  </div>

                  <div className="file-info">

                    <ImageIcon
                      size={16}
                    />

                    <span>
                      {file.name}
                    </span>

                    <small>
                      {
                        (
                          file.size /
                          1024
                        ).toFixed(0)
                      } KB
                    </small>

                  </div>

                  <span>
                    Click to change
                  </span>

                </div>

              ) : (

                <div className="upload-content">

                  <div className="upload-icon-large">
                    <Upload
                      size={27}
                    />
                  </div>

                  <h4>
                    Drop your signature here
                  </h4>

                  <p>
                    or{" "}
                    <b>
                      browse from your device
                    </b>
                  </p>

                  <small>
                    PNG · JPG · JPEG · WEBP
                  </small>

                </div>

              )}

            </div>


            {error && (

              <div className="form-error">
                {error}
              </div>

            )}


            <div className="action-row">

              <button
                className="primary-btn"
                disabled={
                  !file ||
                  loading
                }
                onClick={
                  verify
                }
              >

                <ShieldCheck
                  size={17}
                />

                {loading
                  ? "Analyzing..."
                  : "Verify signature"}

              </button>


              <button
                className="secondary-btn"
                disabled={loading}
                onClick={clear}
              >
                Clear
              </button>

            </div>

          </div>


          <div className="dashboard-card result-card">

            <div className="card-heading">

              <div>

                <h3>
                  Analysis result
                </h3>

                <p>
                  AI prediction and
                  confidence
                </p>

              </div>

            </div>


            {!result &&
              !loading && (

                <div className="empty-result">

                  <ShieldCheck
                    size={48}
                  />

                  <h3>
                    Ready to verify
                  </h3>

                  <p>
                    Upload a signature
                    to see the result.
                  </p>

                </div>

              )}


            {loading && (

              <div className="empty-result">

                <Sparkles
                  size={45}
                />

                <h3>
                  Analyzing signature
                </h3>

                <p>
                  Running the
                  TensorFlow model...
                </p>

              </div>

            )}


            {result && !loading && (

              <div className="result-content">

                <div
                  className={
                    `decision ${
                      genuine
                        ? "genuine"
                        : "forged"
                    }`
                  }
                >

                  <div className="decision-icon">

                    {genuine
                      ? "✓"
                      : "!"}

                  </div>

                  <div>

                    <small>
                      VERIFICATION DECISION
                    </small>

                    <strong>
                      {result.result}
                    </strong>

                  </div>

                </div>


                <div className="confidence-block">

                  <div className="confidence-header">

                    <span>
                      Model confidence
                    </span>

                    <strong>
                      {
                        result.confidence
                      }%
                    </strong>

                  </div>

                  <div className="confidence-track">

                    <div
                      className={
                        genuine
                          ? "genuine-bar"
                          : "forged-bar"
                      }
                      style={{
                        width:
                          `${result.confidence}%`
                      }}
                    />

                  </div>

                </div>


                <div className="probability-grid">

                  <div>

                    <span>
                      Genuine
                    </span>

                    <strong>
                      {
                        result.genuine_probability
                      }%
                    </strong>

                  </div>


                  <div>

                    <span>
                      Forged
                    </span>

                    <strong>
                      {
                        result.forged_probability
                      }%
                    </strong>

                  </div>

                </div>

              </div>

            )}

          </div>

        </div>

      </div>
    </>
  );
}