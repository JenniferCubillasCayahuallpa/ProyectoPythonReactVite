import { Link } from "react-router-dom";
import { FaAngleRight, FaApple } from "react-icons/fa";
import { useAppDispatch, useAppSelector } from "../store/store";
import { closeSideBar } from "../store/sidebarSlice";
import clsx from "clsx";

export const Sidebar = () => {
  const iconSize = 25;

  const isSidebarOpen = useAppSelector((state) => state.isSideBarOpen.value);
  const dispatch = useAppDispatch();

  return (
    <>
      {isSidebarOpen && (
        <div
          className="fade-in absolute top-0 left-0 w-screen 
        h-screen backdrop-blur-xs backdrop-filter z-10"
          onClick={() => dispatch(closeSideBar())}
        />
      )}
      <nav
        className={clsx(
          "h-full w-[200px] px-3 bg-red-50 absolute top-0 -left-[200px] ",
          "transform transition-all duration-300 z-20",
          { "translate-x-[200px]": isSidebarOpen }
        )}
      >
        <div className="h-[100px] p-5 flex justify-center items-center">
          <div className="w-full py-5 flex justify-center items-center border-b border-gray-400">
            <FaApple size={50} />
          </div>
        </div>
        <div className="flex flex-col gap-5">
          <Link
            to={"/"}
            className="flex flex-row mt-5 text-gray-700 hover:text-blue-600 transition-colors"
            onClick={() => dispatch(closeSideBar())}
          >
            <FaAngleRight size={iconSize} />
            <span className="ml-3 text-xl">Inicio</span>
          </Link>
          <Link
            to={"/users"}
            className="flex flex-row mt-5 text-gray-700 hover:text-blue-600 transition-colors"
            onClick={() => dispatch(closeSideBar())}
          >
            <FaAngleRight size={iconSize} />
            <span className="ml-3 text-xl">Usuarios</span>
          </Link>
        </div>
      </nav>
    </>
  );
};
