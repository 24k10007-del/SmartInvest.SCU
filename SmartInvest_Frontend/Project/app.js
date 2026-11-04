const BASE_URL = "http://127.0.0.1:5000/api";
const STOCK_SYMBOL = "TLKM.JK";


document.addEventListener("DOMContentLoaded", () => {
    setupLoginHandler();
    setupNavigation();
    const token = localStorage.getItem("token");

    if (token) {

        document.getElementById("loginPage").style.display = "none";

        document.getElementById("appDashboard").style.display = "flex";

        fetchStockData();

        renderOrderBook();

    }

    document.getElementById("btnExportPdf").addEventListener("click", exportPDF);
    document.getElementById("btnLogout").addEventListener("click", handleLogout);
});

function setupLoginHandler() {

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener("submit", async (e) => {

            e.preventDefault();

            const fullname = document.getElementById("fullname").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirmPassword").value;

            if (password !== confirmPassword) {

                alert("Password tidak sama.");

                return;
            }

            const response = await fetch(`${BASE_URL}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    fullname: fullname,
                    email: email,
                    password: password
                })
            });

            const result = await response.json();

            console.log(result);

            if (response.ok) {
                alert("Registrasi berhasil.");
                window.location.href = "dashboard.html";
            } else {
                alert(result.message || JSON.stringify(result));
            }

        });

    }
    const loginForm = document.getElementById("loginForm");
    const loginPage = document.getElementById("loginPage");
    const appDashboard = document.getElementById("appDashboard");
    const loginError = document.getElementById("loginError");

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {

            const response = await fetch(`${BASE_URL}/auth/login`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })

            });

            const result = await response.json();

            if (response.ok) {

                localStorage.setItem("token", result.token);

                loginPage.style.display = "none";
                appDashboard.style.display = "flex";
                loginError.style.display = "none";

                fetchStockData();
                renderOrderBook();

            } else {

                loginError.style.display = "block";

            }

        } catch (err) {

            console.error(err);
            loginError.style.display = "block";

        }

    });

}

// Fungsi Logout untuk Mengembalikan ke Tampilan Login
function handleLogout() {

    localStorage.removeItem("token");

    document.getElementById("appDashboard").style.display = "none";

    document.getElementById("loginPage").style.display = "flex";

    document.getElementById("username").value = "";

    document.getElementById("password").value = "";

}

async function fetchStockData() {
    try {
        const response = await fetch(`${BASE_URL}/dashboard`);
        const result = await response.json();
        const data = result.data ? result.data : result;
        
        document.getElementById("stockName").innerText =
        data.company.company;

        document.getElementById("stockTicker").innerText =
        data.company.symbol;

        document.getElementById("stockPrice").innerText =
        `Rp ${data.current.currentPrice.toLocaleString('id-ID')}`;

        document.getElementById("aiScore").innerText =
        data.recommendation.score + " pts";

        document.getElementById("aiLabel").innerText =
        data.recommendation.recommendation;

        document.getElementById("aiReason").innerText =
        data.recommendation.reason.join(", ");
        
        renderLineChart(

            ["SMA20","EMA20","Current"],

            [

                data.analysis.SMA20,

                data.analysis.EMA20,

                data.current.currentPrice

            ]

        );
    } catch (error) {
        console.error("Gagal memuat API Utama Saham, menggunakan data historis fallback Telkom:");
    }
}

function renderOrderBook() {
    const bidData = [
        { vol: 14205, price: 2710 },
        { vol: 23140, price: 2700 },
        { vol: 18950, price: 2690 },
        { vol: 32110, price: 2680 },
        { vol: 41050, price: 2670 }
    ];

    const offerData = [
        { price: 2720, vol: 9840 },
        { price: 2730, vol: 15420 },
        { price: 2740, vol: 24105 },
        { price: 2750, vol: 19800 },
        { price: 2760, vol: 35140 }
    ];

    document.getElementById("bidTableBody").innerHTML = bidData.map(item => `
        <tr>
            <td class="text-left">${item.vol.toLocaleString('id-ID')}</td>
            <td class="text-right bid-price">${item.price.toLocaleString('id-ID')}</td>
        </tr>
    `).join('');

    document.getElementById("offerTableBody").innerHTML = offerData.map(item => `
        <tr>
            <td class="text-left offer-price">${item.price.toLocaleString('id-ID')}</td>
            <td class="text-right">${item.vol.toLocaleString('id-ID')}</td>
        </tr>
    `).join('');

    const tradeLogData = [
        { time: "11:29:45", price: 2720, vol: 450, type: "BUY" },
        { time: "11:29:32", price: 2710, vol: 1200, type: "SELL" },
        { time: "11:29:10", price: 2720, vol: 85, type: "BUY" },
        { time: "11:28:55", price: 2720, vol: 600, type: "BUY" },
        { time: "11:28:12", price: 2690, vol: 350, type: "SELL" }
    ];

    document.getElementById("tradeLogTableBody").innerHTML = tradeLogData.map(item => {
        const isBuy = item.type === 'BUY';
        const textColor = isBuy ? 'var(--neon-green)' : 'var(--neon-red)';
        const badgeBg = isBuy ? 'var(--neon-glow-green)' : 'var(--neon-glow-red)';

        return `
            <tr>
                <td class="text-left" style="color: #64748b; font-size: 0.8rem;">${item.time}</td>
                <td class="text-center font-mono" style="text-align: center; font-weight: 600; color: ${textColor};">${item.price.toLocaleString('id-ID')}</td>
                <td class="text-right" style="font-family: monospace;">${item.vol.toLocaleString('id-ID')}</td>
                <td class="text-right">
                    <span style="background: ${badgeBg}; color: ${textColor}; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; display: inline-block; min-width: 45px; text-align: center;">
                        ${item.type}
                    </span>
                </td>
            </tr>
        `;
    }).join('');
}

function renderLineChart(labels, dataPoints) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    const chartGlowGradient = ctx.createLinearGradient(0, 0, 0, 400);
    chartGlowGradient.addColorStop(0, 'rgba(0, 255, 163, 0.25)');
    chartGlowGradient.addColorStop(1, 'rgba(0, 255, 163, 0.0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Harga Saham',
                data: dataPoints,
                borderColor: '#00ffa3',
                borderWidth: 3,
                pointBackgroundColor: '#00ffa3',
                pointBorderColor: '#090d16',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                backgroundColor: chartGlowGradient,
                fill: true,
                tension: 0.35
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: 'rgba(255, 255, 255, 0.02)' }, ticks: { color: '#64748b' } },
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(255, 255, 255, 0.02)' },
                    ticks: { color: '#64748b', callback: (value) => 'Rp ' + value.toLocaleString('id-ID') }
                }
            }
        }
    });
}

function exportPDF() {
    window.open(`${BASE_URL}/export/pdf`, "_blank");
}

function setupNavigation() {
    const menuMapping = {
        "navTerminal": "contentTerminal",
        "navRiwayat": "contentRiwayat",
        "navWatchlist": "contentWatchlist",
        "navPengaturan": "contentPengaturan"
    };

    Object.keys(menuMapping).forEach(navId => {
        const btn = document.getElementById(navId);
        if (btn) {
            btn.addEventListener("click", (e) => {
                e.preventDefault();
                Object.keys(menuMapping).forEach(id => document.getElementById(id).classList.remove("active"));
                btn.classList.add("active");

                Object.values(menuMapping).forEach(cid => {
                    const el = document.getElementById(cid);
                    if (el) el.style.display = "none";
                });

                const target = document.getElementById(menuMapping[navId]);
                if (target) {
                    target.style.display = (menuMapping[navId] === "contentTerminal") ? "grid" : "block";
                }

                if(navId==="navRiwayat"){
                    loadHistory();
                }
            });
        }
    });
}

async function loadHistory() {

    try {

        const response = await fetch(`${BASE_URL}/history`, {

            headers: {

                Authorization:
                    "Bearer " + localStorage.getItem("token")

            }

        });

        const history = await response.json();

        const container =
            document.getElementById("contentRiwayat");

        container.innerHTML =
            `<h3><i class="fa-solid fa-clock-rotate-left"></i> Riwayat Aktivitas</h3>`;

        if (!history.length) {

            container.innerHTML +=
                "<p>Belum ada riwayat.</p>";

            return;

        }

        history.forEach(item => {

            container.innerHTML += `

            <div class="glass-card" style="margin-top:15px">

                <h4>${item.symbol}</h4>

                <p><b>Harga :</b>
                Rp ${Number(item.price).toLocaleString("id-ID")}</p>

                <p><b>Rekomendasi :</b>
                ${item.recommendation}</p>

                <p><b>Confidence :</b>
                ${item.confidence}</p>

                <p><b>Score :</b>
                ${item.score}</p>

            </div>

            `;

        });

    }

    catch(err){

        console.log(err);

    }

}