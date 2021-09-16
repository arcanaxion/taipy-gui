// set global style the traditonal way
export const setStyle = (styleString: string) => {
    const style = document.createElement("style");
    style.textContent = styleString;
    document.head.append(style);
};

export const setDarkMode = (isDarkMode: boolean) => {
    const htmlClasses = document.querySelector("html")?.classList;
    const mode = isDarkMode ? "dark" : "light";
    htmlClasses?.add(mode);
    localStorage.setItem("theme", mode);
};

export const formatWSValue = (value: string, dataType?: string) => dataType === "datetime.datetime" ? new Date(value).toString() : value;

export const ENDPOINT = (!process.env.NODE_ENV || process.env.NODE_ENV === "development") ? process.env.REACT_APP_BACKEND_FLASK_URL : (window as any).flask_url;