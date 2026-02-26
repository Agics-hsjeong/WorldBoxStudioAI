export const load = async () => {
  const apiUrl = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';
  return { apiUrl };
};
