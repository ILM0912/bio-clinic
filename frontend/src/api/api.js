const API_URL = "/api";


const checkResponse = (response) => {
  if (!response.ok) {
    throw new Error(`Ошибка запроса: ${response.status}`);
  }
  return response.json();
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

export const users = [
  {
    id: 1,
    username: "user",
    first_name: "Имя",
    last_name: "Фамилия",
    password: "123",
    role: "user",
  },
  {
    id: 2,
    username: "doctor",
    first_name: "Имя",
    last_name: "Фамилия",
    password: "123",
    role: "doctor",
  },
];

export const login = (username, password) => {
  const user = users.find(
    (u) => u.username === username && u.password === password
  );

  if (!user) {
    return null;
  }

  return {
    id: user.id,
    username: user.username,
    first_name: user.first_name,
    last_name: user.last_name,
    role: user.role,
  };
};