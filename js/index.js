document.addEventListener("DOMContentLoaded", () => {
  // Load all functions
  loadExample();
});

const loadExample = () => {

  const form = document.querySelector("#form");
  const original = document.querySelector("#original");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const file = form.fileInput.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const cont = e.target.result;
      original.innerHTML = cont;
    }
    reader.readAsText(file);
  })
}
