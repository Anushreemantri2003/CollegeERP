import React, { useState, useEffect } from "react";
import { Form, Button, Row, Col, Card, Table, Nav } from "react-bootstrap";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import axios from "../../api/axios";

interface EventType {
  RECORD_ID?: number;
  MAIN_TYPE: string;
  SUB_TYPE: string;
}

const EventTypeMasterForm: React.FC = () => {
  const [eventTypes, setEventTypes] = useState<EventType[]>([]);
  const [activeSection, setActiveSection] = useState("create");
  const [editingId, setEditingId] = useState<number | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<EventType>();

  const fetchEventTypes = async () => {
    try {
      const res = await axios.get("/api/master/event-types/");
      setEventTypes(res.data as EventType[]);
    } catch (err) {
      console.error("Error fetching event types:", err);
    }
  };

  useEffect(() => {
    fetchEventTypes();
  }, []);

  const onSubmit = async (data: EventType) => {
    try {
      if (editingId) {
        await axios.put(`/api/master/event-types/${editingId}/`, data);
        alert("Event Type updated successfully!");
      } else {
        await axios.post("/api/master/event-types/", data);
        alert("Event Type created successfully!");
      }
      reset();
      setEditingId(null);
      fetchEventTypes();
    } catch (err) {
      console.error("Error saving event type:", err);
    }
  };

  const handleEdit = (eventType: EventType) => {
    setEditingId(eventType.RECORD_ID!);
    setValue("MAIN_TYPE", eventType.MAIN_TYPE);
    setValue("SUB_TYPE", eventType.SUB_TYPE);
    setActiveSection("create");
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this event type?")) {
      try {
        await axios.delete(`/api/master/event-types/${id}/`);
        fetchEventTypes();
      } catch (err) {
        console.error("Error deleting event type:", err);
      }
    }
  };

  return (
    <motion.div className="container mt-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <h2 className="mb-4 text-center">Event Type Form</h2>

      <Nav variant="tabs" activeKey={activeSection} onSelect={(k) => setActiveSection(k || "create")}>
        <Nav.Item>
          <Nav.Link eventKey="create">{editingId ? "Edit Event Type" : "Create Event Type"}</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link eventKey="view">View Event Types</Nav.Link>
        </Nav.Item>
      </Nav>

      <Row className="mt-4">
        {activeSection === "create" && (
          <Col md={6}>
            <Card>
              <Card.Header className="bg-primary text-white">
                {editingId ? "Edit Event Type" : "Create Event Type"}
              </Card.Header>
              <Card.Body>
                <Form onSubmit={handleSubmit(onSubmit)}>
                  <Form.Group className="mb-3">
                    <Form.Label>Main Type</Form.Label>
                    <Form.Select {...register("MAIN_TYPE", { required: true })}>
                      <option value="">-- Select Main Type --</option>
                      <option value="Educational">Educational</option>
                      <option value="Non Educational">Non Educational</option>
                    </Form.Select>
                    {errors.MAIN_TYPE && <span className="text-danger">Required</span>}
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Sub Type</Form.Label>
                    <Form.Control type="text" {...register("SUB_TYPE", { required: true })} />
                    {errors.SUB_TYPE && <span className="text-danger">Required</span>}
                  </Form.Group>

                  <Button variant="success" type="submit">
                    {editingId ? "Update" : "Save"}
                  </Button>{" "}
                  <Button
                    variant="secondary"
                    type="button"
                    onClick={() => {
                      reset();
                      setEditingId(null);
                    }}
                  >
                    Clear
                  </Button>
                </Form>
              </Card.Body>
            </Card>
          </Col>
        )}

        {activeSection === "view" && (
          <Col md={8}>
            <Card>
              <Card.Header className="bg-success text-white">View Event Types</Card.Header>
              <Card.Body>
                <Table striped bordered hover responsive>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Main Type</th>
                      <th>Sub Type</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {eventTypes.map((et) => (
                      <tr key={et.RECORD_ID}>
                        <td>{et.RECORD_ID}</td>
                        <td>{et.MAIN_TYPE}</td>
                        <td>{et.SUB_TYPE}</td>
                        <td>
                          <Button
                            variant="warning"
                            size="sm"
                            onClick={() => handleEdit(et)}
                            className="me-2"
                          >
                            Edit
                          </Button>
                          <Button
                            variant="danger"
                            size="sm"
                            onClick={() => handleDelete(et.RECORD_ID!)}
                          >
                            Delete
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        )}
      </Row>
    </motion.div>
  );
};

export default EventTypeMasterForm;
