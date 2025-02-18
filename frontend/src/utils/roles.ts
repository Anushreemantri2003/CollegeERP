export enum Roles {
  Admin = "Admin",
  Teacher = "Teacher",
  Student = "Student",
  Guest = "Guest",
}

export function isAdmin(role: Roles): boolean {
  return role === Roles.Admin;
}

export function isTeacher(role: Roles): boolean {
  return role === Roles.Teacher;
}

export function isStudent(role: Roles): boolean {
  return role === Roles.Student;
}

export function isGuest(role: Roles): boolean {
  return role === Roles.Guest;
}

export const ROLES = {
  SUPERADMIN: "SUPERADMIN",
  ADMIN: "ADMIN",
  COE: "COE",
  HOD: "HOD",
  FACULTY: "FACULTY",
  STUDENT: "STUDENT",
  FINANCE: "FINANCE",
  LIBRARY: "LIBRARY",
  WARDEN: "WARDEN",
  PLACEMENT: "PLACEMENT",
} as const;

export const getDashboardRoute = (role: string | undefined) => {
  console.log("=== Route Selection ===");
  console.log("Input role:", role);

  if (!role) {
    console.log("No role provided, returning to home");
    return "/";
  }

  const upperRole = role.toUpperCase();
  console.log("Normalized role:", upperRole);

  switch (upperRole) {
    case ROLES.SUPERADMIN:
      return "/superadmin-dashboard";
    case ROLES.ADMIN:
      return "/admin-dashboard";
    case ROLES.COE:
      return "/coe-dashboard";
    case ROLES.HOD:
      return "/hod-dashboard";
    case ROLES.FACULTY:
      return "/faculty-dashboard";
    case ROLES.STUDENT:
      return "/student-dashboard";
    case ROLES.FINANCE:
      return "/finance-dashboard";
    case ROLES.LIBRARY:
      return "/library-dashboard";
    case ROLES.WARDEN:
      return "/hostel-dashboard";
    case ROLES.PLACEMENT:
      return "/placement-dashboard";
    default:
      console.warn(`Unknown role: ${upperRole}`);
      return "/";
  }
};
