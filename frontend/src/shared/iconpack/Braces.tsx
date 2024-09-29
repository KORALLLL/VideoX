import { SVGProps } from 'react'

export const Braces = (props: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="none"
    stroke="currentColor"
    stroke-width="1.66667"
    stroke-linecap="round"
    stroke-linejoin="round"
    {...props}
  >
    <path d="M6.66667 2.5H5.83333C5.39131 2.5 4.96738 2.67559 4.65482 2.98816C4.34226 3.30072 4.16667 3.72464 4.16667 4.16667V8.33333C4.16667 8.77536 3.99107 9.19928 3.67851 9.51184C3.36595 9.8244 2.94203 10 2.5 10C2.94203 10 3.36595 10.1756 3.67851 10.4882C3.99107 10.8007 4.16667 11.2246 4.16667 11.6667V15.8333C4.16667 16.75 4.91667 17.5 5.83333 17.5H6.66667M13.3333 17.5H14.1667C14.6087 17.5 15.0326 17.3244 15.3452 17.0118C15.6577 16.6993 15.8333 16.2754 15.8333 15.8333V11.6667C15.8333 10.75 16.5833 10 17.5 10C17.058 10 16.634 9.8244 16.3215 9.51184C16.0089 9.19928 15.8333 8.77536 15.8333 8.33333V4.16667C15.8333 3.72464 15.6577 3.30072 15.3452 2.98816C15.0326 2.67559 14.6087 2.5 14.1667 2.5H13.3333"/>
  </svg>
)
