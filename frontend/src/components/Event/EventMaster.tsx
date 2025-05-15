import React, { useState, useEffect } from "react";
import { Form, Button, Row, Col, Card, Table } from "react-bootstrap";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import axios from "../../api/axios";

interface EventMaster {
  RECORD_ID?: number;
  EVENT_TYPE: number;
  EVENT_NAME: string;
  ORGANIZED_BY: number;
  EVENT_START_DT: string;
  EVENT_END_DT: string;
  EVENT_PURPOSE: string;
  EVENT_REMARKS?: string;
}

const EventMasterForm: React.FC = () => {
  const [eventTypes, setEventTypes] = useState<any[]>([]);
  const [committees, setCommittees] = useState<any[]>([]);
  const [events, setEvents] = useState<EventMaster[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<EventMaster>();

  const fetchData = async () => {
    try {
      const [eventTypesRes, committeesRes, eventsRes] = await Promise.all([
        axios.get("/api/master/event-types/"),
        axios.get<any[]>("/api/master/committees/"),
        axios.get("/api/master/events/"),
      ]);
      setEventTypes(eventTypesRes.data as any[]);
      setCommittees(committeesRes.data);
      setEvents(eventsRes.data as EventMaster[]);
    } catch (err) {
      console.error("Error fetching data:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onSubmit = async (data: EventMaster) => {
    try {
      if (editingId) {
        await axios.put(`/api/master/events/${editingId}/`, data);
        alert("Event updated successfully!");
      } else {
        await axios.post("/api/master/events/", data);
        alert("Event created successfully!");
      }
      reset();
      setEditingId(null);
      fetchData();
    } catch (err) {
      console.error("Error saving event:", err);
    }
  };

  const handleEdit = (event: EventMaster) => {
    setEditingId(event.RECORD_ID || null);
    for (const key in event) {
      setValue(key as keyof EventMaster, event[key as keyof EventMaster]);
    }
  };

  const handleDelete = async (id: number | undefined) => {
    if (!id) return;
    if (window.confirm("Are you sure you want to delete this event?")) {
      try {
        await axios.delete(`/api/master/events/${id}/`);
        alert("Event deleted successfully!");
        fetchData();
      } catch (err) {
        console.error("Error deleting event:", err);
      }
    }
  };

  return (
    <motion.div className="container mt-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <Row>
        <Col md={12}>
          <Card>
            <Card.Header className="bg-primary text-white">
              {editingId ? "Edit Event" : "Create Event"}
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit(onSubmit)}>
                <Row className="mb-3">
                  <Col md={6}>
                    <Form.Label>Event Type</Form.Label>
                    <Form.Select {...register("EVENT_TYPE", { required: true })}>
                      <option value="">-- Select Event Type --</option>
                      {eventTypes.map((et) => (
                        <option key={et.RECORD_ID} value={et.RECORD_ID}>
                          {et.MAIN_TYPE} - {et.SUB_TYPE}
                        </option>
                      ))}
                    </Form.Select>
                    {errors.EVENT_TYPE && <span className="text-danger">Required</span>}
                  </Col>

                  <Col md={6}>
                    <Form.Label>Organized By</Form.Label>
                    <Form.Select {...register("ORGANIZED_BY", { required: true })}>
                      <option value="">-- Select Organizing Committee  --</option>
                      {committees.map((c) => (
                        <option key={c.RECORD_ID} value={c.RECORD_ID}>
                          {c.COM_NAME}
                        </option>
                      ))}
                    </Form.Select>
                    {errors.ORGANIZED_BY && <span className="text-danger">Required</span>}
                  </Col>
                </Row>

                <Row className="mb-3">
                  <Col md={6}>
                    <Form.Label>Event Name</Form.Label>
                    <Form.Control
                      size="sm"
                      type="text"
                      {...register("EVENT_NAME", { required: true })}
                    />
                    {errors.EVENT_NAME && <span className="text-danger">Required</span>}
                  </Col>

                  <Col md={3}>
                    <Form.Label>Start Date</Form.Label>
                    <Form.Control
                      size="sm"
                      type="date"
                      {...register("EVENT_START_DT", { required: true })}
                    />
                    {errors.EVENT_START_DT && <span className="text-danger">Required</span>}
                  </Col>

                  <Col md={3}>
                    <Form.Label>End Date</Form.Label>
                    <Form.Control
                      size="sm"
                      type="date"
                      {...register("EVENT_END_DT", { required: true })}
                    />
                    {errors.EVENT_END_DT && <span className="text-danger">Required</span>}
                  </Col>
                </Row>

                <Row className="mb-3">
                  <Col md={6}>
                    <Form.Label>Event Purpose</Form.Label>
                    <Form.Control
                      size="sm"
                      as="textarea"
                      rows={2}
                      {...register("EVENT_PURPOSE", )}
                    />
                  
                  </Col>

                  <Col md={6}>
                    <Form.Label>Event Remarks</Form.Label>
                    <Form.Control
                      size="sm"
                      as="textarea"
                      rows={2}
                      {...register("EVENT_REMARKS")}
                    />
                  </Col>
                </Row>

                <div className="d-flex justify-content-end gap-2">
                  <Button variant="success" type="submit" size="sm">
                    {editingId ? "Update" : "Save"}
                  </Button>
                  <Button
                    variant="secondary"
                    type="button"
                    size="sm"
                    onClick={() => {
                      reset();
                      setEditingId(null);
                    }}
                  >
                    Clear
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>

          {/* View Section */}
          <Card className="mt-4">
            <Card.Header className="bg-info text-white">View Events</Card.Header>
            <Card.Body>
              <Table striped bordered hover responsive size="sm">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Event Name</th>
                    <th>Type</th>
                    <th>Organized By</th>
                    <th>Start</th>
                    <th>End</th>
                    <th>Purpose</th>
                    <th>Remarks</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((ev, idx) => (
                    <tr key={ev.RECORD_ID}>
                      <td>{idx + 1}</td>
                      <td>{ev.EVENT_NAME}</td>
                      <td>{eventTypes.find((et) => et.RECORD_ID === ev.EVENT_TYPE)?.MAIN_TYPE}</td>
                      <td>{committees.find((c) => c.RECORD_ID === ev.ORGANIZED_BY)?.COM_NAME}</td>
                      <td>{ev.EVENT_START_DT}</td>
                      <td>{ev.EVENT_END_DT}</td>
                      <td>{ev.EVENT_PURPOSE}</td>
                      <td>{ev.EVENT_REMARKS}</td>
                      <td>
                        <Button size="sm" variant="warning" onClick={() => handleEdit(ev)}>
                          Edit
                        </Button>{" "}
                        <Button
                          size="sm"
                          variant="danger"
                          onClick={() => handleDelete(ev.RECORD_ID)}
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
      </Row>
    </motion.div>
  );
};

export default EventMasterForm;
