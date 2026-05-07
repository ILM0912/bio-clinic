import React, { useEffect, useMemo, useState } from "react";

import { createAppointment, getBusySlots } from "../../api/api";
import DoctorChoiceList from "./DoctorChoiceList";
import ButtonFilter from "./ButtonFilter";
import TimeSlotPicker from "./TimeSlotPicker";

const getTodayDate = () => {
  const today = new Date();

  return today.toISOString().split("T")[0];
};

const isWeekend = (dateValue) => {
  const date = new Date(`${dateValue}T00:00:00`);
  const day = date.getDay();
  return day === 0 || day === 6;
};

const isPastDate = (dateValue) => {
  return dateValue < getTodayDate();
};

const getDateError = (dateValue) => {
  if (!dateValue) {
    return "";
  }
  if (isPastDate(dateValue)) {
    return "Нельзя выбрать прошедшую дату.";
  }
  if (isWeekend(dateValue)) {
    return "Запись доступна только в будние дни.";
  }
  return "";
};

function AppointmentForm({ doctorServices }) {
  const [selectedBranchId, setSelectedBranchId] = useState(null);
  const [selectedDoctorServiceId, setSelectedDoctorServiceId] = useState(null);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [busySlots, setBusySlots] = useState([]);
  const [isSlotsLoading, setIsSlotsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const dateError = getDateError(selectedDate);
  const todayDate = getTodayDate();

  const branches = useMemo(() => {
    return doctorServices.reduce((result, item) => {
      const exists = result.some((branch) => branch.id === item.branch.id);
      if (!exists) {
        result.push(item.branch);
      }
      return result;
    }, []);
  }, [doctorServices]);

  const availableDoctors = useMemo(() => {
    if (!selectedBranchId) {
      return [];
    }
    return doctorServices.filter(
      (item) => item.branch.id === selectedBranchId
    );
  }, [doctorServices, selectedBranchId]);

  useEffect(() => {
    if (!selectedDoctorServiceId || !selectedDate || dateError) {
      setBusySlots([]);
      return;
    }
    setIsSlotsLoading(true);
    getBusySlots({
      doctorBranchServiceId: selectedDoctorServiceId,
      date: selectedDate,
    })
      .then((data) => {
        setBusySlots(data.busy_slots || []);
      })
      .catch((requestError) => {
        setBusySlots([]);
        setError(
          requestError.message || "Не удалось загрузить занятые слоты."
        );
      })
      .finally(() => {
        setIsSlotsLoading(false);
      });
  }, [selectedDoctorServiceId, selectedDate, dateError]);

  const handleBranchChange = (branchId) => {
    setSelectedBranchId(branchId);
    setSelectedDoctorServiceId(null);
    setSelectedDate("");
    setSelectedTime("");
    setBusySlots([]);
    setSuccess("");
    setError("");
  };

  const handleDoctorChange = (doctorServiceId) => {
    setSelectedDoctorServiceId(doctorServiceId);
    setSelectedDate("");
    setSelectedTime("");
    setBusySlots([]);
    setSuccess("");
    setError("");
  };

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
    setSelectedTime("");
    setBusySlots([]);
    setSuccess("");
    setError("");
  };

  const handleTimeChange = (time) => {
    setSelectedTime(time);
    setSuccess("");
    setError("");
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!selectedBranchId) {
      setError("Выберите филиал.");
      return;
    }
    if (!selectedDoctorServiceId) {
      setError("Выберите врача.");
      return;
    }
    if (!selectedDate) {
      setError("Выберите дату.");
      return;
    }
    if (dateError) {
      setError(dateError);
      return;
    }
    if (!selectedTime) {
      setError("Выберите время.");
      return;
    }

    const dateTime = `${selectedDate}T${selectedTime}:00`;

    setIsSubmitting(true);

    createAppointment({
      doctorBranchServiceId: selectedDoctorServiceId,
      dateTime,
    })
      .then(() => {
        setSuccess("Запись успешно создана.");
        setSelectedTime("");
      })
      .catch((requestError) => {
        setError(requestError.message || "Не удалось создать запись.");
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  };

  if (doctorServices.length === 0) {
    return (
      <p className="text-muted">
        Для этой услуги пока нет доступных врачей.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
        <ButtonFilter
          title="Филиал"
          items={branches}
          selectedValue={selectedBranchId}
          onChange={handleBranchChange}
          showAll={false}
        />

      {selectedBranchId && (
        <DoctorChoiceList
          doctors={availableDoctors}
          selectedValue={selectedDoctorServiceId}
          onChange={handleDoctorChange}
        />
      )}

      {selectedDoctorServiceId && (
        <div className="mb-4 col-12 col-md-4">
          <label htmlFor="appointment-date" className="form-label fw-semibold">
            Дата
          </label>
          <input
            id="appointment-date"
            type="date"
            className="form-control"
            min={todayDate}
            value={selectedDate}
            onChange={handleDateChange}
          />
          {dateError && (
            <div className="text-danger small mt-2">
              {dateError}
            </div>
          )}
        </div>
      )}

      {selectedDoctorServiceId && selectedDate && !dateError && (
        <>
          {isSlotsLoading && (
            <p className="text-muted">Проверяем занятые слоты...</p>
          )}

          <TimeSlotPicker
            selectedValue={selectedTime}
            busySlots={busySlots}
            selectedDate={selectedDate}
            onChange={handleTimeChange}
          />
        </>
      )}

      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {selectedDoctorServiceId && selectedDate && selectedTime && !dateError && (
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Создание записи..." : "Записаться"}
        </button>
      )}
    </form>
  );
}

export default AppointmentForm;