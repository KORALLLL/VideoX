import { SVGProps } from 'react'

export const Cross = (props: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="18"
    height="18"
    viewBox="0 0 18 18"
    fill="none"
    stroke="currentColor"
    stroke-width="1.5"
    stroke-linecap="round"
    stroke-linejoin="round"
    {...props}
  >
    <path d="M13.5 4.5L4.5 13.5M4.5 4.5L13.5 13.5"/>
  </svg>
)
