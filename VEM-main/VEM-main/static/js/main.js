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
    // Remove existing toast if any
    const existing = document.querySelector('.alert-toast');
    if (existing) {
        existing.remove();
    }

    const toast = document.createElement('div');
    toast.className = `alert-toast ${type}`;
    
    // Set icon based on type
    let icon = '🔔';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    document.body.appendChild(toast);

    // Auto remove after 5 seconds (matched with CSS animation)
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Clean up toasts on click
function initToastCleanup() {
    document.addEventListener('click', (e) => {
        if (e.target.closest('.alert-toast')) {
            e.target.closest('.alert-toast').remove();
        }
    });
}

// --- Real-time Search and Dropdown Filter ---
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

                const searchMatches = searchData.includes(query);
                const statusMatches = statusVal === '' || statusData === statusVal;

                if (classMatches && searchMatches && statusMatches) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Update count badge
            const countBadge = group.querySelector('.group-count');
            if (countBadge) {
                countBadge.textContent = visibleCount;
            }

            // Hide group entirely if empty
            if (visibleCount === 0 || !classMatches) {
                group.style.display = 'none';
            } else {
                group.style.display = '';
            }
        });
    }

    if (searchInput) searchInput.addEventListener('input', filterCards);
    if (classFilter) classFilter.addEventListener('change', filterCards);
    if (statusFilter) statusFilter.addEventListener('change', filterCards);
}

// --- Status Update Modal (Admin Only) ---
function initStatusEditModal() {
    const dialog = document.getElementById('edit-status-dialog');
    if (!dialog) return;

    const form = document.getElementById('edit-status-form');
    const medIdInput = document.getElementById('edit-med-id');
    const medNomeSpan = document.getElementById('edit-med-nome');
    const closeBtn = dialog.querySelector('.dialog-close');
    const cancelBtn = dialog.querySelector('.btn-cancel');

    // Attach click listeners to Edit Status buttons (using event delegation)
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-edit-status');
        if (!btn) return;

        e.preventDefault();
        const medId = btn.dataset.id;
        const medNome = btn.dataset.nome;
        const currentStatus = btn.dataset.status;

        // Set form fields
        medIdInput.value = medId;
        medNomeSpan.textContent = medNome;

        // Select the matching radio button
        const radio = form.querySelector(`input[name="novo_status"][value="${currentStatus}"]`);
        if (radio) {
            radio.checked = true;
        }

        dialog.showModal();
    });

    function closeDialog() {
        dialog.close();
        form.reset();
    }

    if (closeBtn) closeBtn.addEventListener('click', closeDialog);
    if (cancelBtn) cancelBtn.addEventListener('click', closeDialog);

    // Handle Form Submit (AJAX)
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const medId = medIdInput.value;
        const selectedRadio = form.querySelector('input[name="novo_status"]:checked');
        if (!selectedRadio) {
            showToast('Por favor, selecione um status.', 'error');
            return;
        }
        const novoStatus = selectedRadio.value;

        fetch('/api/alterar_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                medicamento_id: parseInt(medId, 10),
                novo_status: novoStatus
            })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(res => {
            if (res.status === 200 && res.body.success) {
                showToast(res.body.message, 'success');
                
                // Dynamically update the row in the table
                const card = document.querySelector(`.med-card[data-id="${medId}"]`);
                if (card) {
                    card.dataset.status = novoStatus; // Update status in dataset for search filtering
                    const badge = card.querySelector('.badge-status');
                    if (badge) {
                        // Keep the SVG or the little dot and just update the text and class
                        badge.className = 'badge-status';
                        if (novoStatus === 'Disponível') badge.classList.add('status-disponivel');
                        else if (novoStatus === 'Indisponível') badge.classList.add('status-indisponivel');
                        else if (novoStatus === 'Estoque baixo') badge.classList.add('status-baixo');
                        else if (novoStatus === 'Aguardando entrega') badge.classList.add('status-aguardando');
                        else if (novoStatus === 'Farmácia Popular') badge.classList.add('status-farmacia-popular');
                        
                        // Render SVG checkmark for "Disponível", else a small dot
                        let iconHtml = '';
                        if (novoStatus === 'Disponível') {
                            iconHtml = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="12" height="12"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`;
                        } else {
                            iconHtml = `<span style="width: 6px; height: 6px; border-radius: 50%; background-color: currentColor;"></span>`;
                        }
                        badge.innerHTML = `${iconHtml} ${novoStatus}`;
                    }
                    
                    // Update dataset on the button itself so opening it again has the correct status checked
                    const editBtn = card.querySelector('.btn-edit-status');
                    if (editBtn) {
                        editBtn.dataset.status = novoStatus;
                    }
                }
                closeDialog();
            } else {
                showToast(res.body.message || 'Erro ao alterar status.', 'error');
            }
        })
        .catch(err => {
            console.error('Error updating status:', err);
            showToast('Erro de conexão ou servidor.', 'error');
        });
    });
}

// --- Create Medication Modal (Admin Only) ---
function initCadastrarModal() {
    const dialog = document.getElementById('cadastrar-med-dialog');
    if (!dialog) return;

    const openBtn = document.getElementById('btn-open-cadastrar');
    const form = document.getElementById('cadastrar-med-form');
    const closeBtn = dialog.querySelector('.dialog-close');
    const cancelBtn = dialog.querySelector('.btn-cancel');

    if (openBtn) {
        openBtn.addEventListener('click', (e) => {
            e.preventDefault();
            dialog.showModal();
        });
    }

    function closeDialog() {
        dialog.close();
        form.reset();
    }

    if (closeBtn) closeBtn.addEventListener('click', closeDialog);
    if (cancelBtn) cancelBtn.addEventListener('click', closeDialog);

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const nome = document.getElementById('cad-nome').value.trim();
        const classificacao = document.getElementById('cad-classificacao').value.trim();
        const posologia = document.getElementById('cad-posologia').value.trim();
        const indicacao = document.getElementById('cad-indicacao').value.trim();
        const status = document.getElementById('cad-status').value;

        if (!nome || !classificacao) {
            showToast('Nome e classificação são obrigatórios.', 'error');
            return;
        }

        fetch('/api/cadastrar_medicamento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nome: nome,
                classificacao: classificacao,
                posologia: posologia,
                indicacao: indicacao,
                status: status
            })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(res => {
            if (res.status === 200 && res.body.success) {
                showToast(res.body.message, 'success');
                closeDialog();
                // Reload the page after a short delay to display the newly added medicine in alphabetical order
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showToast(res.body.message || 'Erro ao cadastrar medicamento.', 'error');
            }
        })
        .catch(err => {
            console.error('Error creating medication:', err);
            showToast('Erro de conexão ou servidor.', 'error');
        });
    });
}

// --- Accordions (e.g. for disease tabs in static guides) ---
function initAccordions() {
    const headers = document.querySelectorAll('.accordion-header');
    
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const isActive = header.classList.contains('active');
            
            // Close all active accordions first
            document.querySelectorAll('.accordion-header').forEach(h => {
                h.classList.remove('active');
                const content = h.nextElementSibling;
                if (content) content.style.maxHeight = null;
            });
            
            // Open clicked accordion if it wasn't active
            if (!isActive) {
                header.classList.add('active');
                const content = header.nextElementSibling;
                if (content) {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            }
        });
    });
}
