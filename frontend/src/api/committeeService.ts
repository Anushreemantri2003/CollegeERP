import axios from "./axios";

export const committeeService = {
  // GET all committees
  getCommittees: () => axios.get("/api/master/committees/"),

  // POST a new committee
  createCommittee: (data: any) =>
    axios.post("/api/master/committees/", data),

  // PUT update existing committee
  updateCommittee: (id: number, data: any) =>
    axios.put(`/api/master/committees/${id}/`, data),

  // DELETE committee by ID
  deleteCommittee: (id: number) =>
    axios.delete(`/api/master/committees/${id}/`),
};

export default committeeService;
