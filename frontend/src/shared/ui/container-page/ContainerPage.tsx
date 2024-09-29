import { ReactNode } from 'react'
import { Flex } from '..'

interface ContainerPageProps {
  children: ReactNode
}

export const ContainerPage = ({
  children
}: ContainerPageProps) => {
  return (
    <Flex
      w="100%"
      h="100%"
      p={'0 122px'}
      flexDir={'column'}
      overflow={'scroll'}
    >
      {children}
    </Flex>
  )
}
