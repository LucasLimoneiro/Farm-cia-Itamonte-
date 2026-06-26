document.addEventListener('DOMContentLoaded', () => {
    // --- Initializations ---
    initSearchFilter();
    initStatusEditModal();
    initCadastrarModal();
    initAccordions();
    initToastCleanup();
});

// --- Toast Alert Notification ---
function showToast(message, type = 'success') {
    const existing = document.querySelector('.alert-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `alert-toast ${type}`;
    let icon = type === 'success' ? '✅' : (type === 'error' ? '❌' : '🔔');
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

function initToastCleanup() {
    document.addEventListener('click', (e) => {
        if (e.target.closest('.alert-toast')) e.target.closest('.alert-toast').remove();
    });
}

// --- Real-time Search ---
function initSearchFilter() {
    const searchInput = document.getElementById('search-input');
    const classFilter = document.getElementById('classification-filter');
    const statusFilter = document.getElementById('status-filter');
    const groups = document.querySelectorAll('.med-group');

    if (!searchInput && !classFilter && !statusFilter) return;

    function filterCards() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const classVal = classFilter ? classFilter.value : '';
        const statusVal = statusFilter ? statusFilter.value : '';

        groups.forEach(group => {
            const groupClass = group.dataset.classification || '';
            const cards = group.querySelectorAll('.med-card');
            let visibleCount = 0;
            const classMatches = classVal === '' || groupClass === classVal;

            cards.forEach(card => {
                const searchData = card.dataset.searchText || '';
                const statusData = card.dataset.status || '';
                if (classMatches && searchData.includes(query) && (statusVal === '' || statusData === statusVal)) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            const countBadge = group.querySelector('.group-count');
            if (countBadge) countBadge.textContent = visibleCount;
            group.style.display = (visibleCount === 0 || !classMatches) ? 'none' : '';
        });
    }

    if (searchInput) searchInput.addEventListener('input', filterCards);
    if (classFilter) classFilter.addEventListener('change', filterCards);
    if (statusFilter) statusFilter.addEventListener('change', filterCards);
}

// --- Status Update Modal ---
function initStatusEditModal() {
    const dialog = document.getElementById('edit-status-dialog');
    const form = document.getElementById('edit-status-form');
    if (!dialog || !form) return;

    dialog.querySelector('.dialog-close')?.addEventListener('click', () => dialog.close());
    dialog.querySelector('.btn-cancel')?.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => {
        if (e.target === dialog) dialog.close();
    });

    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-edit-status');
        if (!btn) return;

        const currentStatus = btn.dataset.status || '';
        document.getElementById('edit-med-id').value = btn.dataset.id;
        document.getElementById('edit-med-nome').textContent = btn.dataset.nome;

        // Reset radio buttons for both potential names
        form.querySelectorAll('input[name="novo_status"]').forEach(r => r.checked = false);
        form.querySelectorAll('input[name="status-base"]').forEach(r => r.checked = false);
        
        const checkPopular = document.getElementById('status-popular');
        if (checkPopular) checkPopular.checked = currentStatus.includes('Farmácia Popular');

        const statusBase = currentStatus.replace(', Farmácia Popular', '').trim();
        
        const radioNew = form.querySelector(`input[name="novo_status"][value="${statusBase}"]`);
        if (radioNew) radioNew.checked = true;
        
        const radioBase = form.querySelector(`input[name="status-base"][value="${statusBase}"]`);
        if (radioBase) radioBase.checked = true;

        dialog.showModal();
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        let novoStatus = '';
        const selectedRadioNew = form.querySelector('input[name="novo_status"]:checked');
        const selectedRadioBase = form.querySelector('input[name="status-base"]:checked');
        
        if (selectedRadioNew) {
            novoStatus = selectedRadioNew.value;
        } else if (selectedRadioBase) {
            novoStatus = selectedRadioBase.value;
            const checkPopular = document.getElementById('status-popular');
            if (checkPopular && checkPopular.checked) novoStatus += ", Farmácia Popular";
        } else {
            const selectOriginal = document.getElementById('novo-status');
            if (selectOriginal) novoStatus = selectOriginal.value;
        }

        fetch('/api/alterar_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ medicamento_id: parseInt(document.getElementById('edit-med-id').value, 10), novo_status: novoStatus })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast(data.message, 'error');
                }
            });
    });
}

// --- Cadastrar Medicamento ---
function initCadastrarModal() {
    const dialog = document.getElementById('cadastrar-med-dialog');
    if (!dialog) return;
    const form = document.getElementById('cadastrar-med-form');
    document.getElementById('btn-open-cadastrar')?.addEventListener('click', () => dialog.showModal());
    dialog.querySelector('.dialog-close')?.addEventListener('click', () => dialog.close());
    dialog.querySelector('.btn-cancel')?.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => {
        if (e.target === dialog) dialog.close();
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let baseStatus = document.getElementById('cad-status').value;
        const isPopular = document.getElementById('cad-popular') && document.getElementById('cad-popular').checked;
        if (isPopular) {
            baseStatus += ", Farmácia Popular";
        }

        const payload = {
            nome: document.getElementById('cad-nome').value.trim(),
            classificacao: document.getElementById('cad-classificacao').value.trim(),
            status: baseStatus
        };
        fetch('/api/cadastrar_medicamento', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast(data.message, 'error');
                }
            });
    });
}

// --- Accordions ---
function initAccordions() {
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const isActive = header.classList.contains('active');
            document.querySelectorAll('.accordion-header').forEach(h => {
                h.classList.remove('active');
                if (h.nextElementSibling) h.nextElementSibling.style.maxHeight = null;
            });
            if (!isActive) {
                header.classList.add('active');
                if (header.nextElementSibling) header.nextElementSibling.style.maxHeight = header.nextElementSibling.scrollHeight + "px";
            }
        });
    });
}