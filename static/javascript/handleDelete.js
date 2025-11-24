const deleteBtn = document.getElementById("keluar");
const modalContainer = document.getElementById("modalConfirmation");
const cancelBtn = document.getElementById("batal");
const phkBtn = document.getElementById("phk");
const resignBtn = document.getElementById("resign");

// Mengambil form sebagai container
const formContainer = document.querySelector(".modal-card form");
const actionButtons = document.querySelector(".modal-actions");

// Fungsi clear dynamic inputs
const clearDynamicInputs = () => {
  // Hapus input date yang sudah ada
  // Hapus description elemen yang sudah ada
  // Hapus status input

  const existingInput = document.getElementById("dynamic-date-input");
  const existingDesc = document.getElementById("dynamic-desc");
  const existingStatus = document.getElementById("status-input");

  if (existingInput) existingInput.remove();
  if (existingDesc) existingDesc.remove();
  if (existingStatus) existingStatus.remove();
};

const createDateInput = (labelText, statusValue) => {
  clearDynamicInputs();

  // 1.  Deskripsi
  const desc = document.createElement("p");
  desc.textContent = labelText;
  desc.id = "dynamic-desc";
  desc.className = "text-secondary mb-1";

  // 2. Input Tanggal
  const dateInput = document.createElement("input");
  dateInput.type = "date";
  dateInput.id = "dynamic-date-input";
  dateInput.name = "tanggal_keluar";

  // 3.Input Hidden buat status (PHK/Resign)
  const statusInput = document.createElement("input");
  statusInput.type = "hidden";
  statusInput.name = "status";
  statusInput.value = statusValue;
  statusInput.id = "status-input";

  const btnSimpan = document.getElementById("btn-simpan");

  if (btnSimpan) {
    btnSimpan.classList.remove("d-none");
    btnSimpan.classList.add("d-flex");
  }

  formContainer.insertBefore(desc, actionButtons);
  formContainer.insertBefore(dateInput, actionButtons);
  formContainer.insertBefore(statusInput, actionButtons);
};

if (deleteBtn) {
  deleteBtn.addEventListener("click", () => {
    modalContainer.style.display = "flex";
  });
}

if (cancelBtn) {
  cancelBtn.addEventListener("click", () => {
    modalContainer.style.display = "none";
    const btnSimpan = document.getElementById("btn-simpan");
    if (btnSimpan) {
      btnSimpan.classList.remove("d-flex");
      btnSimpan.classList.add("d-none");
    }
    clearDynamicInputs();
  });
}

if (phkBtn) {
  phkBtn.addEventListener("click", (e) => {
    e.preventDefault();
    createDateInput("Silahkan masukan tanggal PHK", "PHK");
  });
}

if (resignBtn) {
  resignBtn.addEventListener("click", (e) => {
    e.preventDefault();
    createDateInput("Silahkan masukan tanggal Resign", "Resign");
  });
}
