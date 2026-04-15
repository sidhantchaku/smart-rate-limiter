const API_BASE = window.location.origin;

const elements = {
  form: document.getElementById("login-form"),
  username: document.getElementById("username"),
  password: document.getElementById("password"),
  profileBtn: document.getElementById("profile-btn"),
  callBtn: document.getElementById("call-btn"),
  statusBtn: document.getElementById("status-btn"),
  user: document.getElementById("user"),
  plan: document.getElementById("plan"),
  tokenState: document.getElementById("token-state"),
  response: document.getElementById("response"),
  limit: document.getElementById("limit"),
  remaining: document.getElementById("remaining"),
  reset: document.getElementById("reset"),
  source: document.getElementById("source"),
  meter: document.getElementById("meter"),
};

let accessToken = "";

async function request(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const payload = await response.json();
  if (!response.ok) {
    throw payload;
  }

  return payload;
}

function setSession(user, plan) {
  elements.user.textContent = user;
  elements.plan.textContent = plan;
  elements.tokenState.textContent = accessToken ? "Loaded" : "Missing";
  const enabled = Boolean(accessToken);
  elements.profileBtn.disabled = !enabled;
  elements.callBtn.disabled = !enabled;
  elements.statusBtn.disabled = !enabled;
}

function updateRateLimit(rateLimit) {
  if (!rateLimit) {
    return;
  }

  const used = Math.max(rateLimit.limit - rateLimit.remaining, 0);
  const percentage = rateLimit.limit ? (used / rateLimit.limit) * 100 : 0;

  elements.limit.textContent = rateLimit.limit;
  elements.remaining.textContent = rateLimit.remaining;
  elements.reset.textContent = `${rateLimit.reset_in_seconds}s`;
  elements.source.textContent = rateLimit.source;
  elements.meter.style.width = `${percentage}%`;
}

function renderResponse(data) {
  elements.response.textContent = JSON.stringify(data, null, 2);
}

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({
        username: elements.username.value,
        password: elements.password.value,
      }),
    });

    accessToken = data.access_token;
    setSession(elements.username.value, "top-tier");
    renderResponse(data);
  } catch (error) {
    accessToken = "";
    setSession("Login failed", "-");
    renderResponse(error);
  }
});

elements.profileBtn.addEventListener("click", async () => {
  try {
    const data = await request("/api/auth/me");
    setSession(data.username, data.plan);
    renderResponse(data);
  } catch (error) {
    renderResponse(error);
  }
});

elements.callBtn.addEventListener("click", async () => {
  try {
    const data = await request("/api/protected-api");
    updateRateLimit(data.rate_limit);
    renderResponse(data);
  } catch (error) {
    if (error.detail) {
      renderResponse(error.detail);
      updateRateLimit(error.detail);
      return;
    }
    renderResponse(error);
  }
});

elements.statusBtn.addEventListener("click", async () => {
  try {
    const data = await request("/api/rate-limit/status");
    updateRateLimit(data);
    renderResponse(data);
  } catch (error) {
    renderResponse(error);
  }
});

setSession("Not logged in", "-");
