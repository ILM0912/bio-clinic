const API_URL = "/api";

const getErrorMessage = (data) => {
  if (typeof data === "string") {
    return data;
  }
  if (Array.isArray(data)) {
    return data.join(" ");
  }
  if (typeof data === "object" && data !== null) {
    return Object.values(data).flat().join(" ");
  }
  return "Ошибка запроса";
};

const checkResponse = async (response) => {
  const contentType = response.headers.get("content-type");
  if (!contentType || !contentType.includes("application/json")) {
    if (!response.ok) {
      throw new Error(`Ошибка сервера: ${response.status}`);
    }

    return null;
  }
  const data = await response.json();
  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }
  return data;
};

export const getGroups = () => {
  return fetch(`${API_URL}/groups/`).then(checkResponse);
};

export const getBranches = () => {
  return fetch(`${API_URL}/branches/`).then(checkResponse);
};

export const getServices = ({ branchId = null, groupId = null } = {}) => {
  const params = new URLSearchParams();
  if (branchId) {
    params.set("branch", branchId);
  }
  if (groupId) {
    params.set("group", groupId);
  }
  const queryString = params.toString();
  const url = queryString
    ? `${API_URL}/services/?${queryString}`
    : `${API_URL}/services/`;
  return fetch(url).then(checkResponse);
};

export const getService = (id) => {
  return fetch(`${API_URL}/services/${id}/`).then(checkResponse);
};

export const getDoctors = () => {
  return fetch(`${API_URL}/doctors/`).then(checkResponse);
};

export const register = ({ email, first_name, last_name, password }) => {
  return fetch(`${API_URL}/auth/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      first_name,
      last_name,
      password,
    }),
  }).then(checkResponse);
};

export const login = ({ email, password }) => {
  return fetch(`${API_URL}/auth/token/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  })
    .then(checkResponse)
    .then((data) => {
      localStorage.setItem("auth_token", data.auth_token);
      return fetch(`${API_URL}/auth/users/me/`, {
        headers: {
          Authorization: `Token ${data.auth_token}`,
        },
      });
    })
    .then(checkResponse);
};

export const logout = () => {
  const token = localStorage.getItem("auth_token");
  return fetch(`${API_URL}/auth/token/logout/`, {
    method: "POST",
    headers: {
      Authorization: `Token ${token}`,
    },
  }).finally(() => {
    localStorage.removeItem("auth_token");
  });
};

export const getCurrentUser = () => {
  const token = localStorage.getItem("auth_token");

  return fetch(`${API_URL}/auth/users/me/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  }).then(checkResponse);
};

export const getDoctorServices = (serviceId) => {
  return fetch(`${API_URL}/doctor-services/?service=${serviceId}`).then(
    checkResponse
  );
};

export const getBusySlots = ({ doctorBranchServiceId, date }) => {
  const params = new URLSearchParams();

  params.set("doctor_branch_service", doctorBranchServiceId);
  params.set("date", date);

  return fetch(`${API_URL}/appointments/busy-slots/?${params.toString()}`).then(
    checkResponse
  );
};

export const createAppointment = ({ doctorBranchServiceId, dateTime }) => {
  const token = localStorage.getItem("auth_token");

  return fetch(`${API_URL}/appointments/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
    body: JSON.stringify({
      doctor_branch_service: doctorBranchServiceId,
      date_time: dateTime,
    }),
  }).then(checkResponse);
};