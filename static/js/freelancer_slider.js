const toggleBtn = document.getElementById('toggleSidebar');
const closeBtn = document.getElementById('closeSidebar');
const sidebar = document.getElementById('sidebar');

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('active');
  toggleBtn.classList.toggle('d-none');
});

closeBtn.addEventListener('click', () => {
  sidebar.classList.remove('active');
  toggleBtn.classList.remove('d-none');
});