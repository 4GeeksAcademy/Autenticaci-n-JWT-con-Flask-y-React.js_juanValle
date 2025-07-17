import { publicFetch, privateFetch } from "./apiFetch";

export const login = async (dispatch, email, password) => {
  let response = await publicFetch("/login", "POST", { email, password });
  if (!response.token) {
    return response;
  }
  localStorage.setItem("token", response.token);
  dispatch({ type: "SET_TOKEN", payload: response.token });
  return response;
};

export const logout = async () => {};

export const register = async () => {};

export const getInfo = async (dispatch) => {
  let response = await privateFetch("/userinfo");
  if (response.msg) {
    console.error(response.msg);
    return null;
  }
  dispatch({ type: "SET_USER_INFO", payload: response });
  return response;
};
