import { Outlet } from "react-router-dom";
import { FaAlignJustify } from "react-icons/fa";
import { Sidebar } from "./Sidebar";
import { useAppDispatch } from "../store/store";
import { openSideBar } from "../store/sidebarSlice";

export const Layout = () => {
  const dispatch = useAppDispatch();

  return (
    <div className="w-full lg:w-[1024px] m-auto flex flex-col justify-start relative overflow-hidden min-h-screen">
      <Sidebar />
      <header className="h-14 bg-blue-950 flex flex-row justify-between text-white">
        <div className="w-2/12 flex flex-row justify-center items-center">
          <button
            aria-label="Abrir menú lateral"
            className="bg-transparent hover:bg-blue-500 font-semibold 
          hover:text-white py-2 px-4 border 
          border-white hover:border-transparent rounded active:scale-95"
            onClick={() => dispatch(openSideBar())}
          >
            <FaAlignJustify size={30} />
          </button>
        </div>
        <span className="flex justify-center items-center w-10/12 bg-blue-600">
        </span>
      </header>
      <main className="flex-1 min-h-[600px]">
        <Outlet />
      </main>
      <footer className="h-14 bg-blue-950 flex justify-center items-center text-white">
      </footer>
    </div>
  );
};


