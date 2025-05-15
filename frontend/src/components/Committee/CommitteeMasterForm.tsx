import React, { useState, useEffect } from "react";
import {
  Form,
  Button,
  Row,
  Col,
  Card,
  Table,
  Tabs,
  Tab,
  Container,
} from "react-bootstrap";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import axiosInstance from "../../api/axios";

interface Committee {
  RECORD_ID?: number;
  COM_NAME: string;
  COM_FORMATION_DATE: string;
  ACTIVE: string;
  LEVEL1: string;
  REMARKS: string;
}

const CommitteeMasterForm: React.FC = () => {
  const [key, setKey] = useState("create");
  const [committees, setCommittees] = useState<Committee[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null); // track editing ID

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<Committee>();

  useEffect(() => {
    if (key === "view") fetchCommittees();
  }, [key]);

  const fetchCommittees = async () => {
    try {
      const response = await axiosInstance.get<Committee[]>("/api/master/committees/");
      setCommittees(response.data);
    } catch (error) {
      console.error("Error fetching committees:", error);
    }
  };

  const onSubmit = async (data: Committee) => {
    try {
      if (editingId) {
        await axiosInstance.put(`/api/master/committees/${editingId}/`, data);
        alert("Committee updated successfully!");
      } else {
        await axiosInstance.post("/api/master/committees/", data);
        alert("Committee created successfully!");
      }
      reset();
      setEditingId(null);
      fetchCommittees();
      setKey("view");
    } catch (error) {
      console.error("Submission error:", error);
    }
  };

  const handleEdit = (committee: Committee) => {
    setValue("COM_NAME", committee.COM_NAME);
    setValue("COM_FORMATION_DATE", committee.COM_FORMATION_DATE);
    setValue("ACTIVE", committee.ACTIVE);
    setValue("LEVEL1", committee.LEVEL1);
    setValue("REMARKS", committee.REMARKS);
    setEditingId(committee.RECORD_ID ?? null);
    setKey("create");
  };

  const handleDelete = async (id: number | undefined) => {
    if (!id) return;
    const confirmDelete = window.confirm("Are you sure you want to delete this committee?");
    if (!confirmDelete) return;

    try {
      await axiosInstance.delete(`/api/master/committees/${id}/`);
      alert("Committee deleted successfully!");
      fetchCommittees();
    } catch (error) {
      console.error("Delete error:", error);
    }
  };

  return (
    <Container className="mt-4">
      <Tabs id="committee-tabs" activeKey={key} onSelect={(k) => setKey(k || "create")} className="mb-4">
        <Tab eventKey="create" title={editingId ? "Edit Committee" : "Create Committee"}>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
            <Card>
              <Card.Body>
                <Form onSubmit={handleSubmit(onSubmit)}>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Committee Name</Form.Label>
                        <Form.Control
                          type="text"
                          {...register("COM_NAME", { required: true })}
                          placeholder="Enter name"
                        />
                        {errors.COM_NAME && <span className="text-danger">Required</span>}
                      </Form.Group>
                    </Col>

                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Formation Date</Form.Label>
                        <Form.Control
                          type="date"
                          {...register("COM_FORMATION_DATE", { required: true })}
                        />
                        {errors.COM_FORMATION_DATE && <span className="text-danger">Required</span>}
                      </Form.Group>
                    </Col>

                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Active</Form.Label>
                        <Form.Select {...register("ACTIVE", { required: true })}>
                          <option value="">-- Select --</option>
                          <option value="Y">Yes</option>
                          <option value="N">No</option>
                        </Form.Select>
                        {errors.ACTIVE && <span className="text-danger">Required</span>}
                      </Form.Group>
                    </Col>

                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Level</Form.Label>
                        <Form.Control type="text" {...register("LEVEL1", { required: true })} />
                        {errors.LEVEL1 && <span className="text-danger">Required</span>}
                      </Form.Group>
                    </Col>

                    <Col md={12}>
                      <Form.Group className="mb-3">
                        <Form.Label>Remarks</Form.Label>
                        <Form.Control as="textarea" rows={3} {...register("REMARKS")} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Button type="submit" variant="primary">
                    {editingId ? "Update Committee" : "Save Committee"}
                  </Button>{" "}
                  {editingId && (
                    <Button
                      variant="secondary"
                      onClick={() => {
                        reset();
                        setEditingId(null);
                      }}
                    >
                      Cancel Edit
                    </Button>
                  )}
                </Form>
              </Card.Body>
            </Card>
          </motion.div>
        </Tab>

        <Tab eventKey="view" title="View Committees">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
            <Card>
              <Card.Body>
                {committees.length === 0 ? (
                  <p>No committees found.</p>
                ) : (
                  <Table striped bordered hover responsive>
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Formation Date</th>
                        <th>Active</th>
                        <th>Level</th>
                        <th>Remarks</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {committees.map((com) => (
                        <tr key={com.RECORD_ID}>
                          <td>{com.COM_NAME}</td>
                          <td>{com.COM_FORMATION_DATE}</td>
                          <td>{com.ACTIVE}</td>
                          <td>{com.LEVEL1}</td>
                          <td>{com.REMARKS}</td>
                          <td>
                            <Button
                              variant="warning"
                              size="sm"
                              onClick={() => handleEdit(com)}
                              className="me-2"
                            >
                              Edit
                            </Button>
                            <Button
                              variant="danger"
                              size="sm"
                              onClick={() => handleDelete(com.RECORD_ID)}
                            >
                              Delete
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                )}
              </Card.Body>
            </Card>
          </motion.div>
        </Tab>
      </Tabs>
    </Container>
  );
};

export default CommitteeMasterForm;
